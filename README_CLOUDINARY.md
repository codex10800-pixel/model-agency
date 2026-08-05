Cloudinary setup

This project supports using Cloudinary for media storage. On Render (or any host) you can use Cloudinary's free tier and set the `CLOUDINARY_URL` environment variable.

1. Create a free Cloudinary account: https://cloudinary.com/
2. In Cloudinary dashboard go to "Account Details" and copy the "CLOUDINARY_URL" value.
3. In your Render service settings add an environment variable `CLOUDINARY_URL` with that value.
4. Deploy. Uploaded media files will be served from Cloudinary and persist across deploys.

Notes:
- This uses `django-cloudinary-storage`. The package was added to `requirements.txt`.
- Alternatively, use `django-storages` + S3/Spaces if you prefer AWS/DigitalOcean.
