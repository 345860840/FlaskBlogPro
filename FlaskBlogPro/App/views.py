# url+视图函数
import datetime
import io
import random
import re
import uuid
from PIL import Image as Img,ImageDraw,ImageFont
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, make_response
from sqlalchemy import desc

from App.exts import cache
from .models import *

blog = Blueprint('blog', __name__)
admin = Blueprint('admin', __name__)


@blog.route('/')
def home():
    return 'HOME'

# 主界面
@blog.route('/index/',methods=["GET","POST"])
def index():
    if request.method == "GET":

        user = User.query.get(1)
        imgs = Image.query.all()
        types = Articletype.query.all()

        dlog = Article.query.all()
        data = {
            "user":user,
            "imgs":imgs,
            "types":types,
            "dlog":dlog,
        }
        return render_template('blog/index.html',**data)

    elif request.method == "POST":
        typeid = None
        try:
            typeid = int(request.form.get("typeid"))
        except:
            return "参数有误"
        dlog = Articletype.query.get(typeid).articles

        articlelist = []
        for i in dlog:
            articlelist.append({"id":i.id,"userid":i.userid,"title":i.title,
            "msg":i.msg,"imgpath":i.imgpath,"type":i.type,
            "isshadow":i.isshadow,"status":i.status,
            "readnum":i.readnum,"zan":i.zan,})

        data = {
            "code":1,
            "msg":"success",
            "data":articlelist,
        }
        return jsonify(data)



# 相册界面
@blog.route('/share/',methods=["GET","POST"])
def share():
    if request.method == "GET":


        return render_template('blog/share.html')

    elif request.method == "POST":
        # 默认就是只有1号 取1号的信息
        page = 1
        try:
            page = int(request.form.get("page"))
        except:
            page = 1
        per_page = 8
        imgs = Image.query.paginate(page, per_page, error_out=False)
        print(imgs.pages)
        imglist = []
        for i in imgs.items:
            imglist.append(
                {"id": i.id, "title": i.title, "userid": i.userid,
                 "path": i.path, "detail": i.detail, "time": i.time}
            )
        data = {
            "code": 1,
            "msg": "success",
            "data": {
                "data":imglist,
                "pages":imgs.pages,
                "page":imgs.page,
                "has_prev": imgs.has_prev,
                "has_next": imgs.has_next,

            }
        }
        return jsonify(data)



# 我的日记界面
@blog.route('/list/',methods=["GET","POST"])
def list():
    if request.method == "GET":
        user = User.query.get(1)
        imgs = Image.query.all()
        types = Articletype.query.all()  # 文章类型
        dlog = Article.query.filter(Article.type==2)  # type==2为查询日记
        paihang = Article.query.filter().order_by(desc("readnum")).limit(8)  # 所有文章按点击排行，也就是阅读量排行
        biaoqian = Articlelabel.query.filter().limit(8)  # 标签只取8个
        data = {
            "user": user,
            "types": types,
            "dlog": dlog,
            "paihang":paihang,
            "biaoqian":biaoqian,
        }
        return render_template('blog/list.html',**data)

    elif request.method == "POST":
        pass



# 关于我界面
@blog.route('/about/',methods=["GET","POST"])
def about():
    if request.method == "GET":
        user = User.query.get(1)
        imgs = Image.query.all()
        types = Articletype.query.all()
        data = {
            "user":user,
            "imgs":imgs,
            "types":types,

        }

        return render_template('blog/about.html',**data)

    elif request.method == "POST":
        pass


# 留言界面
@blog.route('/gbook/',methods=["GET","POST"])
def gbook():
    if request.method == "GET":
        user = User.query.get(1)
        imgs = Image.query.all()
        types = Articletype.query.all()
        liuyan = Lmessage.query.filter().order_by(desc("time"))
        data = {
            "user": user,
            "imgs": imgs,
            "types": types,
            "liuyan":liuyan,
        }

        return render_template('blog/gbook.html',**data)

    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        msg = request.form.get("msg")
        if name and email and msg:
            lmsg = Lmessage()  # 建立新的留言
            lmsg.name = name
            lmsg.email = email
            lmsg.msg = msg
            lmsg.time = datetime.datetime.now()
            db.session.add(lmsg)
            db.session.commit()
            liuyan = Lmessage.query.filter().order_by(desc("time"))
            llist = []   # 重新返回留言信息
            for i in liuyan:
                llist.append({"name":i.name,"msg":i.msg,
                              "time":i.time,"msgback":i.msgback,})

            return jsonify(data={"code": 1, "msg": "success", "data": llist})
            # return redirect(url_for("blog.gbook"))  # 重定向不会弄
        else:
            return jsonify(data = {"code": 0,"msg": "error","data": []})


# 内容页面界面1
@blog.route('/info/<re("(\d)*"):id>',methods=["GET","POST"])
def info(id=1):
    try:
        id = int(id)
    except:
        id = 1
    if request.method == "GET":

        user = User.query.get(1)
        types = Articletype.query.all()  # 文章类型
        paihang = Article.query.filter().order_by(desc("readnum")).limit(8)  # 所有文章按点击排行，也就是阅读量排行
        biaoqian = Articlelabel.query.filter().limit(8)  # 标签只取8个
        article = Article.query.get(id)
        article.readnum+=1
        comts = Comment.query.filter(Comment.articleid==id)
        comments = []
        for i in comts:
            comments.append({"name":i.name,"msg":i.msg,"time":i.time,})
        list = []
        lanmu = ""
        if article.type:  # 如果文章类型存在
            lanmu = Articletype.query.get(article.type).title  # 则写道lanmu中
        al = Alabel.query.filter(Alabel.articleid == article.id)  # 在三方表中查找标签集
        for j in al:  # 遍历查找到的标签集
            lab = Articlelabel.query.get(j.labelid)  # 把标签集里的标签id放入
            if lab:  # 如果标签存在
                list.append(lab.labelname)
        data = {
            "user": user,
            "types": types,
            "paihang": paihang,
            "biaoqian": biaoqian,
            "comments": comments,
            "article":{"articleid": article.id, "lanmu": lanmu, "labels": list,"article": article, },
        }
        db.session.commit()
        return render_template('blog/info.html',**data)

    elif request.method == "POST":
        zanid = request.form.get("zan")
        username = request.form.get("username")
        key = request.form.get("key")
        saytext = request.form.get("saytext")


        if key:
            if not (key.lower() == (cache.get(request.remote_addr+"vcode")).lower()):
                return "验证码错误"
        elif key=="":
            return "验证码错误"
        if username and key and saytext:
            if key.lower() == (cache.get(request.remote_addr+"vcode")).lower():
                comment = Comment()
                comment.articleid=id
                comment.name = username
                comment.msg = saytext
                comment.time = datetime.datetime.now()
                db.session.add(comment)
                db.session.commit()
                return redirect("/info/%s"%id)
            else:
                return "验证码错误"

        try:
            if zanid:
                zanid = int(zanid)
        except:
            zanid = None
        if zanid and not (username or key or saytext):
            if not cache.get(request.remote_addr+"zan"):
                cache.set(request.remote_addr+"zan",[])
            ca = cache.get(request.remote_addr+"zan")
            if id not in ca:
                article = Article.query.get(zanid)
                article.zan += 1
                db.session.commit()
                ca.append(id)

                cache.set(request.remote_addr+"zan",ca,timeout=60*60*24)   # 设置一个ip一天只能赞一篇文章一次
            else:
                return "一天只能赞一次哦"

        return "ok"


# 内容页面界面2
@blog.route('/infopic/',methods=["GET","POST"])
def infopic():
    if request.method == "GET":
        return render_template('blog/infopic.html')

    elif request.method == "POST":
        pass




# --------------------------------------管理员--------------------------------------------  #


# 管理登录
@admin.route('/admin/login/',methods=["POST","GET"])
def admin_login():
    if request.method == "GET":
        return render_template('admin/login.html')
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        adm = Admin.query.filter(Admin.username==username,Admin.password==password).first()
        if adm:
            token = request.cookies.get("token")
            tok = AdminToken.query.filter(AdminToken.admin == adm.id).first()
            res = redirect(url_for("admin.admin_index"))
            if tok:
                uid = uuid.uuid4().hex
                tok.token = uid
                tok.outtime = (datetime.datetime.now()+datetime.timedelta(days=1))
                res.set_cookie("token",uid,max_age=60*60*24)
                db.session.commit()

            else:
                tok = AdminToken()
                tok.admin = adm.id
                tok.token = uuid.uuid4().hex
                tok.outtime = (datetime.datetime.now() + datetime.timedelta(days=1))
                res.set_cookie("token",str(tok.token),max_age=60*60*24)
                print(tok,type(tok))
                db.session.add(tok)
                db.session.commit()
            return res

        else:
            data = {
                "error":"输入的账号或密码有误",
            }
            return render_template('admin/login.html',**data)


# 管理首页
@admin.route('/admin/index/')
def admin_index():
    return render_template('admin/index.html')


# 文章管理
@admin.route('/admin/article/<int:num>/',methods=["POST","GET"])
def admin_article(num):
    if request.method == "GET":
        page = num
        per_page = 8
        articles = Article.query.filter().order_by(desc("time")).offset((page-1)*per_page).limit(per_page)  # 排序数据
        articles1 = Article.query.paginate(page,per_page,error_out=False)  # 带有分页的数据
        label = []
        for i in articles:  # 对文章集合遍历
            lanmu = ""
            if i.type:  # 如果文章类型存在
                lanmu = Articletype.query.get(i.type).title  # 则写道lanmu中
            al = Alabel.query.filter(Alabel.articleid == i.id) # 在三方表中查找标签集
            list = []    # 存的有文章对象+栏目+标签
            for j in al: # 遍历查找到的标签集
                lab = Articlelabel.query.get(j.labelid)  # 把标签集里的标签id放入
                if lab: # 如果标签存在
                    list.append(lab.labelname)
            label.append({"articleid":i.id,"lanmu":lanmu,"labels":list,
                          "article":i,})

        return render_template('admin/article.html',articles=articles,articles1=articles1,label=label)
    elif request.method == "POST":
        return "ok"


# 添加文章
@admin.route('/admin/addarticle/',methods=["POST","GET"])
def admin_addarticle():
    if request.method == "GET":
        type = Articletype.query.filter(Articletype.level==1)  # 一级栏目
        data = []
        for i in type:
            childs = Articletype.query.filter(Articletype.father == i.id)  # 查找子栏目
            data.append(childs)
        return render_template('admin/add-article.html',type=type,data=data)
    elif request.method == "POST":
        title = request.form.get("title")
        msg = request.form.get("content")
        keywd = request.form.get("keywords")
        descri = request.form.get("describe")
        type = request.form.get("category")
        tags = request.form.get("tags")
        titlepic = request.files.get("titlepic")
        isshadow = request.form.get("visibility")
        time = datetime.datetime.now()
        if isshadow=="0":
            isshadow = False
        else:
            isshadow = True
        article = Article()
        article.userid = 1   #  暂时默认为添加用户 1  的文章
        article.title = title
        article.msg = msg
        article.keywd = keywd
        article.descri = descri
        article.type = type
        article.imgpath = ""
        article.isshadow = isshadow
        article.time = time
        article.status = True   # 文章状态改为true
        db.session.add(article)
        db.session.commit()

        tags = re.split(r'(?:,|;|\s)\s*',tags)  # 标签分隔符
        for tag in tags:
            lab = Articlelabel.query.filter(Articlelabel.labelname==tag).first()
            if not lab:
                label = Articlelabel()
                label.labelname = tag
                db.session.add(label)
                db.session.commit()
                alabel = Alabel()
                alabel.articleid = article.id
                alabel.labelid = label.id
                db.session.add(alabel)
                db.session.commit()
            else:
                if not Alabel.query.filter(Alabel.labelid==lab.id,Alabel.articleid==article.id):
                    alabel = Alabel()
                    alabel.articleid = article.id
                    alabel.labelid = lab.id
                    db.session.add(alabel)
                    db.session.commit()

        return redirect("/admin/article/1/")


# 修改文章
@admin.route('/admin/updatearticle/<int:id>/',methods=["POST","GET"])
def admin_updatearticle(id):
    if request.method == "GET":
        article = Article.query.get(id)
        print("-----------------",article)
        type = Articletype.query.filter(Articletype.level == 1)  # 一级栏目
        data = []
        for i in type:
            childs = Articletype.query.filter(Articletype.father == i.id)  # 查找子栏目
            data.append(childs)
        return render_template("admin/update-article.html",article=article,type=type,data=data)
    elif request.method == "POST":

        title = request.form.get("title")
        msg = request.form.get("content")
        keywd = request.form.get("keywords")
        descri = request.form.get("describe")
        type = request.form.get("category")
        tags = request.form.get("tags")
        titlepic = request.files.get("titlepic")   # 其实是图片
        isshadow = request.form.get("visibility")
        time = datetime.datetime.now()
        if isshadow=="0":
            isshadow = False
        else:
            isshadow = True
        article = Article.query.get(id)
        article.title = title
        article.msg = msg
        article.keywd = keywd
        article.descri = descri
        article.type = type

        # article.imgpath = ""
        article.isshadow = isshadow
        article.time = time

        tags = re.split(r'(?:,|;|\s)\s*', tags)  # 标签分隔符
        for tag in tags:
            label = Articlelabel.query.filter(Articlelabel.labelname==tag).first()
            if label:   # 如果这个标签存在了
                alabel = Alabel.query.filter(Alabel.articleid==id,Alabel.labelid==label.id).first()
                if not alabel:   # 如果不存在关联关系则添加关系
                    al = Alabel()
                    al.labelid = label.id
                    al.articleid = id
                    db.session.add(al)
                    db.session.commit()

            else:  # 如果这个标签不存在
                label = Articlelabel()   # 先添加标签
                label.labelname = tag
                db.session.add(label)
                db.session.commit()
                al = Alabel()    # 再添加关联
                al.labelid = label.id
                al.articleid = id
                db.session.add(al)
                db.session.commit()

        return redirect("/admin/article/1/")



# 删除文章
@admin.route('/admin/delarticle/',methods=["POST","GET"])
def admin_delarticle():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        id = request.form.get("id")
        try:
            id = int(id)
        except:
            return "数据类型错误"
        article = Article.query.get(id)  # 一个文章
        alabel = Alabel.query.filter(Alabel.articleid==id)  # 多个标签
        comments = Comment.query.filter(Comment.articleid==id)  # 多条评论
        for i in alabel:
            db.session.delete(i)
            db.session.commit()
        for i in comments:
            db.session.delete(i)
            db.session.commit()
        db.session.delete(article)
        db.session.commit()

        return redirect("/admin/article/1/")



# 公告
@admin.route('/admin/notice/')
def admin_notice():
    return render_template('admin/notice.html')

# 评论
@admin.route('/admin/comment/')
def admin_comment():
    return render_template('admin/comment.html')

# 留言


# 栏目管理
@admin.route('/admin/category/',methods=["GET","POST"])
def admin_category():
    if request.method == "GET":
        type = Articletype.query.filter(Articletype.level == 1)
        data = []
        for i in type:
            childs = Articletype.query.filter(Articletype.father == i.id)
            data.append(childs)
        return render_template('admin/category.html',type=type,data=data)
    elif request.method == "POST":
        title = request.form.get("title")
        othertitle = request.form.get("othertitle")
        father = request.form.get("father")
        keywd = request.form.get("keywd")
        info = request.form.get("info")   # 这是栏目描述
        level = 1
        try:
            father = int(father)
        except:
            father = 0
        if father == 0:   # 不选父类，，则为添加一个等级为1的父类
            father = None
        else:
            level = int(Articletype.query.get(father).level) + 1
        articletype = Articletype()
        articletype.title = title
        articletype.othertitle = othertitle
        articletype.father = father
        articletype.keywd = keywd
        articletype.info = info
        articletype.level = level
        db.session.add(articletype)
        db.session.commit()

        return redirect("/admin/category/")

# 栏目修改
@admin.route('/admin/updatecategory/<int:id>/',methods=["GET","POST"])
def admin_updatecategory(id):
    if request.method == "GET":
        articletype = Articletype.query.get(id)   # 当前需要修改的栏目
        type = Articletype.query.filter(Articletype.level == 1)  # 可选的父亲分类
        print(type.first())
        return render_template("admin/update-category.html",articletype=articletype,type=type)
    elif request.method == "POST":
        title = request.form.get("title")
        othertitle = request.form.get("othertitle")
        father = request.form.get("father")
        keywd = request.form.get("keywd")
        info = request.form.get("info")  # 这是栏目描述
        level = 1
        try:
            father = int(father)
        except:
            father = 0
        if father == 0:  # 不选父类，，则为添加一个等级为1的父类
            father = None
        else:
            level = int(Articletype.query.get(father).level) + 1
        articletype = Articletype.query.get(id)
        articletype.title = title
        articletype.othertitle = othertitle
        articletype.father = father
        articletype.keywd = keywd
        articletype.info = info
        articletype.level = level
        db.session.commit()

        return redirect("/admin/category/")

# 栏目删除
@admin.route('/admin/delcategory/',methods=["GET","POST"])
def admin_delcategory():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        id = request.form.get("id")
        try:
            id = int(id)
        except:
            return "参数异常"
        articletype = Articletype.query.get(id)
        if articletype.level == 1:
            artt = Articletype.query.filter(Articletype.father==articletype.id)
            if artt:
                for i in artt:
                    db.session.delete(i)
                db.session.commit()
            db.session.delete(articletype)
            db.session.commit()

        return redirect("/admin/category/")


# 其他  -友情链接和访问记录
@admin.route('/admin/flink/')
def admin_flink():
    return render_template('admin/flink.html')

# 访问记录


# 用户

@admin.route('/admin/manageuser/')
def admin_manageuser():
    return render_template('admin/manage-user.html')

# 管理登录记录
@admin.route('/admin/loginlog/')
def admin_loginlog():
    return render_template('admin/loginlog.html')



# 基本设置
@admin.route('/admin/setting/')
def admin_setting():
    return render_template('admin/setting.html')

# 阅读设置

@admin.route('/admin/readset/')
def admin_readset():
    return render_template('admin/readset.html')


# 查询管理是否登录中间件
@admin.before_request
def before():
    urls = ["/admin/index/","/admin/category/","/admin/article/","/admin/addarticle/","/admin/updatearticle/",
            "/admin/delcategory/","/admin/updatecategory/","/admin/delcategory/"]
    if request.path in urls:
        token = request.cookies.get("token")
        tok = AdminToken.query.filter(AdminToken.token == token).first()
        if not tok:
            return redirect(url_for("admin.admin_login"))

        if tok.outtime < datetime.datetime.now():
            return redirect(url_for("admin.admin_login"))


# 验证码
@blog.route('/vcode/<re("(\d)*?"):num>',methods=["GET","POST"])
def vcode(num):
    img = Img.new("RGB",(100,50),(200,200,200))
    draw = ImageDraw.Draw(img,"RGB")

    font_path = "App/static/fonts/ADOBEARABIC-BOLD.OTF"
    font = ImageFont.truetype(font=font_path,size=30)
    vcode = random_code()
    cache.set(request.remote_addr+"vcode",vcode,60*60)  # 设置该ip的验证码缓存
    for i in range(len(vcode)):
        xy = (10+i*20,random.randint(-10,20))
        draw.text(xy,vcode[i],font=font,fill=random_color())

    buff = io.BytesIO()
    img.save(buff,"png") # 画布装维png格式的图片，保存到buff缓冲区中

    response = make_response(buff.getvalue())
    response.headers["Content-Type"] = "image/png"
    return response


def random_code():
    s = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    code = ""
    for i in range(4):
        code += random.choice(s)
    return code

def random_color():
    return random.randint(0,255),random.randint(0,255),random.randint(0,255)