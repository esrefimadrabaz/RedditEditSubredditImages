import praw
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import textwrap

reddit = praw.Reddit(client_id = "CLIENT-ID",
                     client_secret = "CLIENT-SECRET",
                     user_agent="USER-AGENT")
z = 0

CaptionsFolder = open('resources/captions.txt', 'wb')
for submissions in reddit.subreddit("INSERT_SUBREDDIT_HERE").top("day", limit = 9):
    if (not submissions.is_self) and (not submissions.over_18):
        _caption = submissions.title
        _name = submissions.author
        _sublink=submissions.url
        _likes = submissions.score
        
        filename = _sublink.split('/')[-1]        
        r = requests.get(_sublink, allow_redirects=True)
        open(filename, 'wb').write(r.content)                       
        
        if filename.endswith('.jpg') or filename.endswith('.png'):
            images_list  = ['resources/black.jpg', filename]
            imgs = [Image.open(i) for i in images_list]
            min_img_width = min(i.width for i in imgs)
            total_height = 0        

            if imgs[1].width > min_img_width or imgs[0].width > min_img_width:
                imgs[1] = imgs[1].resize((min_img_width, int(imgs[1].height / imgs[1].width * min_img_width)), Image.ANTIALIAS)      
                imgs[0] = imgs[0].resize((min_img_width, int(imgs[1].height / 5)), Image.ANTIALIAS)
            total_height = imgs[1].height + imgs[0].height
            img_merge = Image.new(imgs[0].mode, (min_img_width, total_height))
            y = 0
            img_merge.paste(imgs[0], (0, 0))
            img_merge.paste(imgs[1], (0, imgs[0].height))



            ortayükseklik = int(imgs[0].height) / 3
            ortagenislik =  int(min_img_width) / 2
            draw = ImageDraw.Draw(img_merge)
            if (int(img_merge.height) > 800):
                yazı_font = ImageFont.truetype('verdana.ttf', 49, encoding='UTF-8')
            elif (int(img_merge.height) > 1200):
                yazı_font = ImageFont.truetype('verdana.ttf', 66, encoding='UTF-8')
            elif (int(img_merge.width) < 500):
                yazı_font = ImageFont.truetype('verdana.ttf', 20, encoding='UTF-8')
            else:
                yazı_font = ImageFont.truetype('verdana.ttf', 22, encoding='UTF-8')
            n = 0
            lines = textwrap.wrap(str(_caption), width= 30)
            for line in lines:
                width, height = yazı_font.getsize(line)
                w, h = draw.textsize(line, font=yazı_font)
                draw.text((ortagenislik - (w/2), 0 + (h/2) + n), line, fill='white', font=yazı_font)
                n += height
            
                

            _image = img_merge
            _imageBlack = Image.open('resources/black.jpg')            
            total_height2 = 0
            _imageBlack = _imageBlack.resize((min_img_width, int(_image.height / 20)))           
            total_height2 = _image.height + _imageBlack.height
            img_merge2 = Image.new(_image.mode, (min_img_width, total_height2))
            q = int(_image.height)
            img_merge2.paste(_imageBlack, (q, 0))
            img_merge2.paste(_image) 

            alt_orta_x = min_img_width / 6
            alt_orta_y = total_height2 - (int(_imageBlack.height) / 2)
            draw2 = ImageDraw.Draw(img_merge2)
            if (int(img_merge.height) > 800):
                _font2 = ImageFont.truetype('verdana.ttf', 38, encoding='UTF-8')
            elif (int(img_merge.height) > 1200):
                _font2 = ImageFont.truetype('verdana.ttf', 58, encoding='UTF-8')
            else:
                _font2 = ImageFont.truetype('verdana.ttf', 22, encoding='UTF-8')
            a, b = draw2.textsize('u/' + str(_name), font = _font2)
            draw2.text((alt_orta_x - (a/2) , alt_orta_y - (b/2)), "u/" + str(_name), fill='white', font = _font2, align='center')  #useri yazmak icin
            c, d = draw2.textsize(str(_likes), font = _font2)
            draw2.text(((min_img_width / 2) - (c/2) , alt_orta_y - (b/2)), str(_likes), fill='white', font = _font2, align='center')  #_likes yazmak icin
            
            
            upvote = Image.open('resources/upvote.png')
            
            upvote_size_x = int(d + (d/5))

            upvote_yeri_x = (min_img_width / 2) - c - (upvote_size_x / 3)
            upvote_size_y = int(d + (d/5))
            upvote = upvote.resize((upvote_size_x, upvote_size_y))
            img_merge2.paste(upvote, (int(upvote_yeri_x), int(alt_orta_y - (upvote_size_y / 2))), mask = upvote)
            
            logo = Image.open('resources/logo.png')
            logo_yeri_x = alt_orta_x * 5.5
            logo_size_y = int(b * 1.25)
            logo_size_x = int(logo_size_y * 2)
            logo = logo.resize((logo_size_x, logo_size_y))
            img_merge2.paste(logo, (int(logo_yeri_x - (logo_size_x / 2)), int(alt_orta_y - (upvote_size_y / 2))), mask = logo)
            


            max1 = 1080, 1080
            max2 = 1080, 1350
            kontrol_height = int(img_merge2.height)
            kontrol_width = int(img_merge2.width)
                 

            bum = imgs[1]
            img_merge2.thumbnail(max1, Image.ANTIALIAS)
            _newheight = int(img_merge2.height)
            _newwidth = int(img_merge2.width)   

            img_merge2.save(str(z) + '.jpg')

            
            #alta ve üste siyah çizgi koy
            if (_newheight > _newwidth):
                _Fill = 1080 - _newwidth
                img_merge3 = Image.new(_image.mode, (_newwidth + _Fill, _newheight))
                _blackFill = bum.resize((_newwidth + _Fill, _newheight))
                _blackFill1 = _blackFill.crop((0, 0, int(_Fill / 2), _newheight))
                _blackFill1 = _blackFill1.filter(ImageFilter.GaussianBlur(radius=10))
                _blackFill2 = _blackFill.crop((_newwidth - int(_Fill / 2), 0, _newwidth, _newheight))
                _blackFill2 = _blackFill2.filter(ImageFilter.GaussianBlur(radius=10))
                img_merge3.paste(_blackFill1, (0,0))
                img_merge3.paste(img_merge2, (int(_Fill / 2), 0))
                img_merge3.paste(_blackFill2, ((int(_Fill / 2)) + _newwidth, 0))
                img_merge3.save(str(z) + '.jpg')
            elif (_newwidth > _newheight):
                _Fill = 1080 - _newheight
                img_merge3 = Image.new(_image.mode, (_newwidth, (_newheight + _Fill)))
                _blackFill = bum.resize((_newwidth, (_newheight + _Fill)))
                _blackFill1 = _blackFill.crop((0, 0, _newwidth, int(_Fill / 2)))
                _blackFill1 = _blackFill1.filter(ImageFilter.GaussianBlur(radius=10))
                _blackFill2 = _blackFill.crop((0, _newheight - int(_Fill / 2), _newwidth, _newheight))
                _blackFill2 = _blackFill2.filter(ImageFilter.GaussianBlur(radius=10))
                img_merge3.paste(_blackFill1, (0,0))
                img_merge3.paste(img_merge2, (0, int(_Fill / 2)))
                img_merge3.paste(_blackFill2, ((0, (int(_Fill / 2)) + _newheight)))
                img_merge3.save(str(z) + '.jpg')



            if (kontrol_height < 1080) and (kontrol_width < 1080):
                img_merge2.thumbnail(max1, Image.ANTIALIAS)
                _newheight = int(img_merge2.height)
                _newwidth = int(img_merge2.width)
                if (_newheight > _newwidth):
                    _Fill = _newheight - _newwidth
                    img_merge3 = Image.new(_image.mode, (_newwidth + _Fill, _newheight))
                    _blackFill = bum.resize((_newwidth + _Fill, _newheight))
                    _blackFill1 = _blackFill.crop((0, 0, int(_Fill / 2), _newheight))
                    _blackFill1 = _blackFill1.filter(ImageFilter.GaussianBlur(radius=10))
                    _blackFill2 = _blackFill.crop((_newwidth - int(_Fill / 2), 0, _newwidth, _newheight))
                    _blackFill2 = _blackFill2.filter(ImageFilter.GaussianBlur(radius=10))
                    img_merge3.paste(_blackFill1, (0,0))
                    img_merge3.paste(img_merge2, (int(_Fill / 2), 0))
                    img_merge3.paste(_blackFill2, ((int(_Fill / 2)) + _newwidth, 0))
                    img_merge3.save(str(z) + '.jpg')

                elif (_newwidth > _newheight):                
                    _Fill = _newwidth - _newheight
                    img_merge3 = Image.new(_image.mode, (_newwidth, _newheight + _Fill))
                    _blackFill = bum.resize((_newwidth, (_newheight + _Fill)))
                    _blackFill1 = _blackFill.crop((0, 0, _newwidth, int(_Fill / 2)))
                    _blackFill1 = _blackFill1.filter(ImageFilter.GaussianBlur(radius=10))
                    _blackFill2 = _blackFill.crop((0, _newheight - int(_Fill / 2), _newwidth, _newheight))
                    _blackFill2 = _blackFill2.filter(ImageFilter.GaussianBlur(radius=10))
                    img_merge3.paste(_blackFill1, (0,0))
                    img_merge3.paste(img_merge2, (0, int(_Fill / 2)))
                    img_merge3.paste(_blackFill2, (0, (int(_Fill / 2)) + _newheight))
                    img_merge3.save(str(z) + '.jpg')
            
            
            CaptionsFolder.write(str(submissions.title).encode('utf-8'))
            CaptionsFolder.write(os.linesep.encode())    
                             
            os.remove(filename)
            z = z + 1
            if z == 13:
                break
            elif z<13:
                continue
                
            else:
                print("hata")
        os.remove(filename)

sayi = open('resources/count.txt', 'w')
sayi.write(str(z - 1))
CaptionsFolder.close()




        
