# -*- coding: utf-8 -*-

"""
Helper functions to assist file upload to db using boottle, sqlachemy
Requires specific class definition as :

class Upload(Base, MkMixin):
    id = Column(BigInteger, Sequence('gn_upload'), primary_key=True)
    uuid = Column(String(40), unique=True)
    file_name = Column(String(200))
    ext = Column(String(20))
    cnt = deferred(Column(BLOB))
    cnt_th = deferred(Column(BLOB))
    notes = Column(TEXT)
    mimetype = Column(String(100))

__author__ : Çağatay Tengiz
__date__   : 10.01.2014
"""


from uuid import uuid1

import mimetypes
import os
from PIL import Image
from sqlalchemy import Sequence
import io


def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def normalize_filename(afilename):
    return afilename.replace(' ', '_').\
        replace('ç', 'c').replace('Ç', 'c').\
        replace('ı', 'i').replace('İ', 'i').\
        replace('ğ', 'g').replace('Ğ', 'g').\
        replace('ü', 'u').replace('Ü', 'u').\
        replace('ş', 's').replace('Ş', 's').\
        replace('ö', 'o').replace('Ö', 'o').\
        lower().\
        decode('utf-8')


def resize_image(img, basewidth, thumb=False):
    if type(img) == str:
        #resmi file like in memory nesneye atalım
        fx = io.StringIO(img)
    else:
        img.seek(0)
        fx = img

    #daha sonra o temp dosyadan image'ı okuyoruz
    temp_img = Image.open(fx)
    #resmin type'ını alıyoruz (jpeg,png,gif etc.) #imghdr.what(fx)
    file_type = temp_img.format

    if thumb:
        size = basewidth, basewidth
        temp_img.thumbnail(size, Image.ANTIALIAS)
    else:
        if temp_img.size[0] >= basewidth:
            wpercent = (basewidth / float(temp_img.size[0]) )
            hsize = int((float(temp_img.size[1]) * float(wpercent)))
            temp_img = temp_img.resize((basewidth, hsize), Image.ANTIALIAS)

    #image nesnesini buffer'a alıp string'e çeviriyoruz
    buf = io.BytesIO()
    temp_img.save(buf, file_type)
    #tempImg.save(buf, fileType, optimize=True, quality=80)
    return buf.getvalue()


def upload_file(db,
                upload_class,
                afile,
                defi,
                old_id=None,
                upload_path="",
                thumb_size=200,
                image_size=1024,
                store_in_db=False):

    if not afile:
        return 0

    if old_id:
        arw = db.query(upload_class).filter(upload_class.id == old_id).first()
        uuid = arw.uuid
    else:
        arw = upload_class()
        db.add(arw)
        arw.id = db.execute(Sequence('gn_upload'))
        uuid = uuid1()

    #split and chooses the last part (the filename with extension)
    _filename = afile.filename.replace('\\', '/').split('/')[-1]
    _ext = os.path.splitext(_filename)[1].lower()
    _is_image = _ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    arw.uuid = uuid
    arw.file_name = _filename
    arw.ext = _ext
    arw.mimetype = mime_type(_filename)

    arw.defi = defi

    if _is_image:
        cnt_thb = resize_image(afile.file, thumb_size, True)  #thumbnail
        cnt_bin = resize_image(afile.file, image_size)        #Orjinal Boy
    else:
        afile.file.seek(0)
        cnt_bin = afile.file.read()
        cnt_thb = None

    #write the file to disk
    if store_in_db:
        arw.cnt = cnt_bin
        arw.cnt_th = cnt_thb
    else:
        save_path = upload_path
        file_path = "{path}/{file}".format(path=save_path, file=uuid)
        thumb_path = "{path}/th_{file}".format(path=save_path, file=uuid)

        fout = open(file_path, 'wb')
        fout.write(cnt_bin)
        fout.close()

        #Write thumbnail to disk
        if cnt_thb:
            fout = open(thumb_path, 'wb')
            fout.write(cnt_thb)
            fout.close()

    db.commit()

    return arw.id


def convert_db_images():
    from sqlalchemy.orm import scoped_session, sessionmaker
    dbsession = scoped_session(sessionmaker(bind=dbcon.engine))

    imgs = dbsession.query(dbcon.CmsUpload).all()

    for x in imgs:
        if x.cnt:
            cnt_thb = resize_image(x.cnt, 200, True)
            #write the file to disk
            fout = open(config.BASE_PATH + '/uploads/th_' + x.uuid, 'wb')
            fout.write(cnt_thb)
            fout.close()

            cnt2 = resize_image(x.cnt, 1024, True)
            #write the file to disk
            fout = open(config.BASE_PATH + '/uploads/' + x.uuid, 'wb')
            fout.write(cnt2)
            fout.close()


def convert_dir_images():
    imgs = os.listdir(config.BASE_PATH + '/uploads')
    for x in imgs:
        if x[0] != 't':
            fl = open(config.BASE_PATH + '/uploads/' + x, 'rb')
            cnt_thb = resize_image(fl, 200, True)
            #write the file to disk
            fout = open(config.BASE_PATH + '/uploads/th_' + x, 'wb')
            fout.write(cnt_thb)
            fout.close()

            cnt2 = resize_image(fl, 1024, True)
            #write the file to disk
            fout = open(config.BASE_PATH + '/uploads/' + x, 'wb')
            fout.write(cnt2)
            fout.close()

