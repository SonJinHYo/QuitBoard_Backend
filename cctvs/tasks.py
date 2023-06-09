from .models import CCTV
from violations.models import ViolationInfo, Violation
from celery import shared_task

import shutil
import boto3
import os
import imageio
import zipfile
from PIL import Image

s3 = boto3.client("s3")
s3_resource = boto3.resource("s3")


def save_and_get_images_address(dir_name: str) -> str:
    """이미지 폴더 명을 받아서 gif파일 저장후 gif파일 주소를 변환하는 함수
    Args:
        target_dir (str) : gif파일로 만들 이미지가 들어있는 주소
        gif_address (str) : gif 이미지의 주소
        filename (str) : 이미지파일명 (ex. 0_0_114.jpg)
    Return:
        None
    """

    images = []
    image_nums = []
    target_dir = f"/srv/QuitBoard_Backend/tmp/images/{dir_name}"
    gif_address = f"/srv/QuitBoard_Backend/tmp/images/{dir_name}.gif"

    for filename in sorted(os.listdir(target_dir)):
        image_nums.append(int(filename[:-4]))

        image_path = os.path.join(target_dir, filename)
        image = Image.open(image_path)
        images.append(image)

    imageio.mimsave(gif_address, images, **{"duration": 100, "loop": 0})

    middle_image_file = str(len(images) // 2 * 3 - 1).zfill(4) + ".jpg"
    jpg_file_address = (
        f"/srv/QuitBoard_Backend/tmp/images/{dir_name}/{middle_image_file}"
    )

    return jpg_file_address, gif_address


@shared_task
def task_save_violation_data(dir_name: str, region: str, text: str) -> None:
    """DB에 위반정보를 저장하는 함수
    Args:
        dir_name (str) : 읽은 텍스트 파일과 같은 이름의 이미지 폴더
        region (str) : 위반 지역
        text (str) : 위반 사항과 위반 시간을 담은 문자열 (ex. text = 0010,2023-04-23T15:45:43)
        violation_list (list) : 현재 저장된 위반 사항
        violations,time (str) : text를 , 기준으로 나누어 위반 사항과 시간을 저장한 변수
        v_set (set) : 위반 사항을 전부 담은 집합
        image_name (str) : 이미지는 filename과 같은 이름으로 확장자만 png로 다르기 때문에 filename의 확장자면 변경하여 image_name으로 저장한 변수
        image_time (str) : DB에는 초단위까지 시간을 저장하지만 S3폴더에 일자별로 저장하기 위해 년월일 단위까지 따로 일자를 저장
        bucket,key (str) : 버킷 이름, 하위 위치
        v (django_Model_object) : DB에 저장할 django모델 객체

    Return:
        None

    """

    violation_list = [obj.name for obj in Violation.objects.all()]
    violations, time = text.split(",")
    v_set = {violation_list[idx] for idx, i in enumerate(violations) if i == "1"}

    image_time = time[: time.find("T")]
    jpg_file_address, gif_file_address = save_and_get_images_address(dir_name)
    bucket, key = "quit-board-bucket", f"images/{image_time}/{dir_name}.gif"

    # home경로의 aws key를 통해 s3버킷에 파일 업로드
    s3.upload_file(Filename=gif_file_address, Bucket=bucket, Key=key)  # gif 파일
    s3.upload_file(
        Filename=jpg_file_address, Bucket=bucket, Key=key[:-3] + "jpg"
    )  # jpg 파일 (카드 메인 이미지)

    # 업로드한 파일의 이미지 경로를 포함하여 위반객체(ViolationaInfo) 생성 후 One-to-Many관계(Violation-ViolationInfo) 추가
    v = ViolationInfo.objects.create(
        cctv=CCTV.objects.get(region=region),
        detected_time=time,
        img=f"https://{bucket}.s3.ap-northeast-2.amazonaws.com/{key}",
    )
    v.violations.set([obj for obj in Violation.objects.all() if obj.name in v_set])

    return None


@shared_task
def task_rm_zip(zip_address):
    shutil.rmtree(zip_address)


@shared_task
def check_zip_dir():
    bucket = "quit-board-bucket"
    obj_list = s3.list_objects(Bucket=bucket, Prefix="zip_dir/")
    contents = obj_list["Contents"]

    for content in contents:
        key = content["Key"]
        zip_file = s3_resource.Object(bucket, key)
        with zip_file.open() as zip_content:
            with zipfile.ZipFile(zip_content, "r") as zip_ref:
                zip_ref.extractall("/srv/QuitBoard_Backend/tmp")
                vio_dir = "/srv/QuitBoard_Backend/tmp/violations"
                for filename in os.listdir(vio_dir):
                    with open(os.path.join(vio_dir, filename), "r") as f:
                        content = f.read()
                        # 위반 사항이 있는 데이터는 데이터 저장 함수를 통해 저장
                        if int(content[: content.find(",")]) != 0:
                            task_save_violation_data.delay(
                                filename[:-4],
                                # violation_file.cctv.region,
                                content,
                            )
                # 조회가 끝나면 임시 폴더 삭제
                task_rm_zip.delay("/srv/QuitBoard_Backend/tmp")
        # 업데이트가 끝난 데이터를 다시 조회하지 않도록 객체 삭제
        violation_file.delete()
        # task_admin_message(request, "파일 업데이트를 완료하였습니다.")
