import hashlib

import cloudinary
import cloudinary.uploader

from src.conf.config import settings


class UploadService:
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    @staticmethod
    def create_name(email: str, prefix: str):
        name = hashlib.sha256(email.encode()).hexdigest()[:12]
        return f"{prefix}/{name}"

    @staticmethod
    def upload(file, public_id):
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r
    
    @staticmethod
    def upload_video(file, public_id):
        r = cloudinary.uploader.upload(file, resource_type="video", public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_url(public_id, version, width, height):
        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            width=width, height=height, crop="fill", version=version
        )
        return src_url

    @staticmethod
    def get_video_url(public_id, version):
        src_url = cloudinary.CloudinaryVideo(public_id).build_url(version=version)
        return src_url

    @staticmethod
    def add_filter(url, filtername):
        transformed_image = cloudinary.uploader.upload(
            url, transformation=[{"effect": filtername}]
        )
        return transformed_image["url"]
