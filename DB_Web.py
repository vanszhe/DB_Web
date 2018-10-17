import flask
import config
from exts import db
from models import User, Board, Post, Comment, Favorite, ReportP, ReportC
from decorators import login_required
from datetime import date, timedelta, datetime

app = flask.Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')  # 主页
def home():
    allposts = Post.query.all()
    for each in allposts:
        if each.status == 'hot':
            if date.today()-each.post_day > timedelta(days=7):
                each.status = 'normal'
    context = {
        'hots': Post.query.order_by('-id').filter(Post.status == 'normal').all()
    }
    return flask.render_template('home.html', **context)


@app.route('/login/', methods=['GET', 'POST'])  # 登录
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        user = User.query.filter(User.name == username).first()
        if user:
            if user.level < 0:
                return flask.redirect(flask.url_for('failed', info='登录失败...您还需要在小黑屋继续反省！'))
            else:
                if user.password == password:
                    # 将已登录用户保存到浏览器的cookie中
                    flask.session['user_id'] = user.id
                    # 31天内免登录
                    flask.session.permanent = True
                    if flask.request.form.get('remember') == 'on':
                        print(123)
                    return flask.redirect(flask.url_for('total'))
                else:
                    return flask.redirect(flask.url_for('failed', info='登录失败...密码错误！'))
        else:
            return flask.redirect(flask.url_for('failed', info='登录失败...该用户不存在！'))


@app.route('/register/', methods=['GET', 'POST'])  # 注册
def register():
    if flask.request.method == 'GET':
        return flask.render_template('register.html')
    else:
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        password_ = flask.request.form.get('password_')

        user = User.query.filter(User.name == username).first()
        if user:
            # 用户名不能重复
            return flask.redirect(flask.url_for('failed', info='注册失败...该用户名已被占用！'))
        else:
            # 两次密码必须相等
            if password != password_:
                return flask.redirect(flask.url_for('failed', info='注册失败...两次密码输入不同！'))
            else:
                new_user = User(name=username, password=password)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    # 注册成功跳转到登录页面
                    return flask.redirect(flask.url_for('login'))
                except Exception as e:
                    db.session.rollback()
                    return flask.redirect(flask.url_for('failed', info='注册失败...请稍后重新尝试！'))


@app.route('/post/', methods=['GET', 'POST'])  # 发帖
@login_required
def post():
    if flask.request.method == 'GET':
        return flask.render_template('post.html')
    else:
        title = flask.request.form.get('title')
        content = flask.request.form.get('content')
        bid = flask.request.form.get('bid')

        # html中添加版块选项
        # board_id = flask.request.form.get('board_id')
        # board_id = 1

        if title and content:
            user_id = flask.session.get('user_id')
            # 找到版块
            if bid:
                board = Board.query.filter(Board.id == bid).first()
                if board:
                    pass
                else:
                    board = Board.query.filter(Board.id == 1).first()
            else:
                board = Board.query.filter(Board.id == 1).first()

            article = Post(title=title, content=content, author_id=user_id, board_id=board.id)
            user = User.query.filter(User.id == user_id).first()
            article.author = user
            article.board = board
            try:
                db.session.add(article)
                db.session.commit()
                return flask.redirect(flask.url_for('total'))
            except Exception as e:
                db.session.rollback()
                return flask.redirect(flask.url_for('failed', info='发帖失败...请稍后重新尝试！'))
        else:
            return flask.redirect(flask.url_for('failed', info='发帖失败...请输入标题和正文！'))


@app.route('/logout/')  # 退出登录
@login_required
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))


@app.route('/total/')  # 全帖浏览页
def total():
    context = {
        'posts': Post.query.order_by('-id').filter(Post.status != 'reviewing', Post.status != 'blocked').all()
    }
    return flask.render_template('total.html', **context)


@app.route('/board/<board_id>/')  # 全帖浏览页
def sortpost(board_id):
    the_board = Board.query.filter(Board.id == board_id).first()
    if the_board:
        context = {
            'posts': Post.query.order_by('-id').filter(Post.status != 'reviewing', Post.status != 'blocked', Post.board_id == board_id).all(),
            'the_board': the_board
        }
        return flask.render_template('sortpost.html', **context)


@app.route('/boardmag/')
def boardmag():
    context = {
        'boards': Board.query.order_by('id').all()
    }
    return flask.render_template('boardmag.html', **context)


@app.route('/alteradmin/<board_id>')
def alteradminpage(board_id):
    context = {
        'board': Board.query.filter(Board.id == board_id).first()
    }
    return flask.render_template('alteradmin.html', **context)


@app.route('/detail/<post_id>/')  # 某帖详情页
def detail(post_id):
    the_post = Post.query.filter(Post.id == post_id).first()
    user_id = flask.session.get('user_id')
    in_favorites = False
    if user_id:
        for each in the_post.be_favored_by:
            if each.user_id == user_id:
                in_favorites = True
                break
    return flask.render_template('detail.html', article=the_post, favoriteflag=in_favorites)


@app.route('/comment/', methods=['POST'])
@login_required
def comment():
    content = flask.request.form.get('comment')

    user_id = flask.session.get('user_id')
    user = User.query.filter(User.id == user_id).first()

    article_id = flask.request.form.get('post_id')
    article = Post.query.filter(Post.id == article_id).first()
    floor = article.com_num
    parent = 0

    the_comment = Comment(content=content, author_id=user, post_id=article, floor=floor, parent=parent)
    the_comment.author = user
    the_comment.article = article

    article.com_num = article.com_num + 1
    if article.com_num > 20:
        article.author.exp = article.author.exp+3
        if article.author.exp >= article.author.level * 10:
            article.author.exp = article.author.exp - article.author.level * 10
            article.author.level = article.author.level + 1
    if article.com_num > 30:
        if date.today() - article.post_day < timedelta(days=7):
            article.status = 'hot'
    try:
        db.session.add(the_comment)
        db.session.commit()
        return flask.redirect(flask.url_for('detail', post_id=article_id))
    except Exception as e:
        db.session.rollback()
        return flask.redirect(flask.url_for('failed', info='评论失败...请稍后重新尝试！'))


@app.route('/adminuser/')
@login_required
def admin():
    context = {
        'admins': User.query.order_by('id').filter(User.is_admin == 'Y')
    }
    return flask.render_template('adminuser.html', **context)


@app.route('/blackuser/')
@login_required
def black():
    context = {
        'blacks': User.query.order_by('id').filter(User.level < 0)
    }
    return flask.render_template('blackuser.html', **context)


@app.route('/headuser/')
@login_required
def head():
    context = {
        'heads': Board.query.order_by('id').all()
    }
    return flask.render_template('headuser.html', **context)


@app.route('/reviewing/')
@login_required
def reviewing():
    context = {
        'reviews': Post.query.order_by('id').filter(Post.status == 'reviewing').all()
    }
    return flask.render_template('reviewpost.html', **context)


@app.route('/blackpost/')
@login_required
def blackpost():
    context = {
        'blackps': Post.query.order_by('-id').filter(Post.status == 'blocked').all()
    }
    return flask.render_template('blockpost.html', **context)


@app.route('/blackcomments/')
@login_required
def blackcomment():
    context = {
        'blackcs': Comment.query.order_by('-id').filter(Comment.status == 'blocked').all()
    }
    return flask.render_template('blockcomment.html', **context)


@app.route('/userinfo/<user_id>')
def userinfo(user_id):
    the_user = User.query.filter(User.id == user_id).first()
    if the_user:
        context = {
            'the_user': the_user
        }
        return flask.render_template('userinfopage.html', **context)
    else:
        return flask.redirect(flask.url_for('failed', info='无法查看...该用户不存在！'))


@app.route('/alterpasswdpage/')
@login_required
def alterpasswdpage():
    return flask.render_template('alterpassword.html')


@app.route('/altergender/<newgender>/')
@login_required
def altergender(newgender):
    user_id = flask.session.get('user_id')
    the_user = User.query.filter(User.id == user_id).first()
    try:
        the_user.gender = newgender
        db.session.commit()
        return flask.redirect(flask.url_for('succeeded', info='修改成功！您已完善了个人信息！'))
    except Exception as e:
        db.session.rollback()
        return flask.redirect(flask.url_for('failed', info='修改失败...请稍后重新尝试！'))


@app.route('/alterdob/')
@login_required
def alterdob():
    new_y = flask.request.args.get('year')
    new_m = flask.request.args.get('month')
    new_d = flask.request.args.get('day')
    user_id = flask.session.get('user_id')
    the_user = User.query.filter(User.id == user_id).first()
    if new_d or new_m or new_y:
        if new_y != 'None':
            the_year = int(new_y)
        elif the_user.birthday:
            the_year = the_user.birthday.year
        else:
            the_year = date.today().year

        if new_m != 'None':
            the_month = int(new_m)
        elif the_user.birthday:
            the_month = the_user.birthday.month
        else:
            the_month = date.today().month

        if new_d != 'None':
            the_day = int(new_d)
        elif the_user.birthday:
            the_day = the_user.birthday.day
        else:
            the_day = date.today().day

        try:
            new_dob = date(year=the_year, month=the_month, day=the_day)
            if new_dob:
                the_user.birthday = new_dob
                db.session.commit()
            return flask.redirect(flask.url_for('succeeded', info='修改失败...预祝你生日快乐！'))
        except Exception as e:
            return flask.redirect(flask.url_for('failed', info='修改失败...请稍后重新尝试！'))

    else:
        return flask.redirect(flask.url_for('failed', info='修改失败...没有任何改变！'))


@app.route('/alterpasswd/<user_id>/', methods=['POST'])
@login_required
def alterpasswd(user_id):
    the_user = User.query.filter(User.id == user_id).first()
    passwd = flask.request.form.get('passwd')
    newpasswd = flask.request.form.get('newpasswd')
    newpasswdagain = flask.request.form.get('newpasswdagain')
    if passwd == the_user.password:
        if newpasswd == newpasswdagain:
            try:
                the_user.password = newpasswd
                db.session.commit()
                return flask.redirect(flask.url_for('succeeded', info='修改成功！请牢记新密码！'))
            except Exception as e:
                db.session.rollback()
                return flask.redirect(flask.url_for('failed', info='修改失败...请稍后重新尝试！'))
        else:
            return flask.redirect(flask.url_for('failed', info='修改失败...两次密码输入不一致！'))
    else:
        return flask.redirect(flask.url_for('failed', info='修改失败...密码错误！'))


@app.route('/addadmin/', methods=['POST'])
@login_required
def addadmin():
    newname = flask.request.form.get('newname')

    user = User.query.filter(User.name == newname).first()
    if user and user.level >= 0:
        try:
            user.is_admin = 'Y'
            db.session.commit()
            return flask.redirect(flask.url_for('succeeded', info='任命成功！一位新的管理员已经就职！'))
        except Exception as e:
            db.session.rollback()
            return flask.redirect(flask.url_for('failed', info='修改失败...请稍后重新尝试！'))
    else:
        return flask.redirect(flask.url_for('failed', info='任命失败...该用户不存在或者在小黑屋！'))


@app.route('/addblck/', methods=['POST'])
@login_required
def addblack():
    newblack = flask.request.form.get('newblack')
    user = User.query.filter(User.name == newblack).first()
    if user:
        try:
            if user.managed:
                user.managed.admin_id = 1;
            user.is_admin = 'N'
            user.level = 0-user.level
            db.session.commit()
            return flask.redirect(flask.url_for('succeeded', info='封号成功！这位用户已经被关进小黑屋！'))
        except Exception as e:
            db.session.rollback()
            return flask.redirect(flask.url_for('failed', info='封号失败...请稍后重新尝试！'))
    else:
        return flask.redirect(flask.url_for('failed', info='封号失败...该用户不存在！'))


@app.route('/addboard/', methods=['POST'])
@login_required
def addboard():
    new_name = flask.request.form.get('newboard')
    if new_name:
        new_head = flask.request.form.get('newhead')
        new_admin = User.query.filter(User.name == new_head).first()
        if new_admin:
            admin_id = new_admin.id
        else:
            admin_id = 1
        existed = Board.query.filter(Board.name == new_name).first()
        if existed:
            return flask.redirect(flask.url_for('failed', info='添加失败...该版块已存在！'))
        else:
            new_board = Board(name=new_name, admin_id=admin_id)
            try:
                db.session.add(new_board)
                db.session.commit()
                return flask.redirect(flask.url_for('succeeded', info='添加成功！新版块已经成立！'))
            except Exception as e:
                db.session.rollback()
                return flask.redirect(flask.url_for('failed', info='添加失败...请稍后重新尝试！'))
    else:
        return flask.redirect(flask.url_for('failed', info='添加失败...请输入新版块名称！'))


@app.route('/dismiss/<admin_id>/')
@login_required
def dismiss(admin_id):
    print(admin_id)
    if admin_id == '1':
        return flask.redirect(flask.url_for('failed', info='罢免失败...君权神授永世长存！'))
    else:
        the_admin = User.query.filter(User.id == admin_id).first()
        the_admin.is_admin = 'N'
        return flask.redirect(flask.url_for('succeeded', info='罢免成功！前任管理员已经卸任！'))


@app.route('/ban/<user_id>/')
@login_required
def ban(user_id):
    cur_id = flask.session.get('user_id')
    if user_id == cur_id or user_id == '1':
        return flask.redirect(flask.url_for('failed', info='封号失败...您的操作可能越俎代庖了！'))
    else:
        the_user = User.query.filter(User.id == user_id).first()
        try:
            the_user.level = 0-the_user.level
            if the_user.managed:
                the_user.managed.admin_id = 1
            the_user.is_admin = 'N'
            the_user.recognition = None
            db.session.commit()
            return flask.redirect(flask.url_for('succeeded', info='封号成功！这位用户已经被关进小黑屋！'))
        except Exception as e:
            db.session.rollback()
            return flask.redirect(flask.url_for('failed', info='封号失败...请稍后重新尝试！'))


@app.route('/release/<user_id>/')
@login_required
def release(user_id):
    the_user = User.query.filter(User.id == user_id).first()
    try:
        the_user.level = 0-the_user.level
        the_user.is_admin = 'N'
        db.session.commit()
        return flask.redirect(flask.url_for('succeeded', info='解封成功！这位用户已经重获天日了！'))
    except Exception as e:
        db.session.rollback()
        return flask.redirect(flask.url_for('failed', info='解封失败...请稍后重新尝试！'))


@app.route('/normalpost/<post_id>/')
@login_required
def normalpost(post_id):
    the_post = Post.query.filter(Post.id == post_id).first()
    try:
        the_post.status = 'normal'
        db.session.commit()
        return flask.redirect(flask.url_for('succeeded', info='审核通过！这篇帖子已经可以供大家阅览了！'))
    except Exception as e:
        db.session.rollback()
        return flask.redirect(flask.url_for('failed', info='通过失败...请稍后重新尝试！'))


@app.route('/normalcomt/<com_id>')
@login_required
def normalcomt(com_id):
    the_comment = Comment.query.filter(Comment.id == com_id).first()
    if the_comment.like_num > 50:
        the_comment.status = 'hot'
    else:
        the_comment.status = 'normal'
    return flask.redirect(flask.url_for('succeeded', info='审核通过！这条评论已经可以供大家阅览了！'))


@app.route('/blockedpost/<post_id>/')
@login_required
def blockedpost(post_id):
    the_post = Post.query.filter(Post.id == post_id).first()
    try:
        the_post.status = 'blocked'
        db.session.commit()
        return flask.redirect(flask.url_for('succeeded', info='屏蔽成功！这篇帖子可能涉嫌敏感信息已被隐藏！'))
    except Exception as e:
        db.session.rollback()
        return flask.redirect(flask.url_for('failed', info='屏蔽失败...请稍后重新尝试！'))


@app.route('/blockedcomment/<comment_id>/')
@login_required
def blockedcomment(comment_id):
    the_comment = Comment.query.filter(Comment.id == comment_id).first()
    try:
        the_comment.status = 'blocked'
        db.session.commit()
        return flask.redirect(flask.url_for('succeeded', info='屏蔽成功！这条评论可能涉嫌敏感信息已被隐藏！'))
    except Exception as e:
        db.session.rollback()
        return flask.redirect(flask.url_for('failed', info='屏蔽失败...请稍后重新尝试！'))


@app.route('/alteradmin/<board_id>/', methods=['POST'])
@login_required
def alteradmin(board_id):
    the_board = Board.query.filter(Board.id == board_id).first()
    new_name = flask.request.form.get('adminname')
    admin_user = User.query.filter(User.name == new_name).first()
    if the_board and admin_user and admin_user.level >= 0 and admin_user.is_admin == 'Y':
        try:
            the_board.admin_id = admin_user.id
            # the_board.admin = admin_user
            db.session.commit()
            return flask.redirect(flask.url_for('succeeded', info='修改成功！新任管理员已经就职！'))
        except Exception as e:
            db.session.rollback()
            return flask.redirect(flask.url_for('failed', info='修改失败...请稍后重新尝试！'))
    else:
        return flask.redirect(flask.url_for('failed', info='修改失败...管理员的选择可能出现了问题！'))


@app.route('/likeit/<com_id>')
@login_required
def likeit(com_id):
    the_comment = Comment.query.filter(Comment.id == com_id).first()
    try:
        the_comment.like_num = the_comment.like_num+1
        the_user = the_comment.author
        the_user.exp = the_user.exp+1
        if the_user.exp >= the_user.level*10:
            the_user.exp = the_user.exp-the_user.level*10
            the_user.level = the_user.level+1
        if the_comment.like_num >= 50:
            the_comment.status = 'hot'
        db.session.commit()
        return flask.redirect(flask.url_for('detail', post_id=the_comment.article.id))
    except Exception as e:
        db.session.rollback()
        return flask.redirect(flask.url_for('failed', info='点赞失败...请稍后重新尝试！'))


@app.route('/favorone/<post_id>')
@login_required
def favorone(post_id):
    user_id = flask.session.get('user_id')
    try:
        new_favorite = Favorite(user_id=user_id, post_id=post_id)
        db.session.add(new_favorite)
        article = Post.query.filter(Post.id == post_id).first()
        article.favor_num = article.favor_num+1
        db.session.commit()
        return flask.redirect(flask.url_for('succeeded', info='收藏成功！记得常去收藏夹看看！'))
    except Exception as e:
        db.session.rollback()
        return flask.redirect(flask.url_for('failed', info='收藏失败...请稍后重新尝试！'))


@app.route('/search/')
def search():
    keyword = flask.request.args.get('keyword')
    if keyword:
        the_posts = Post.query.order_by('-id').filter(Post.title.contains(keyword), Post.status != 'blocked', Post.status != 'reviewing').all()
        the_users = User.query.filter(User.name.contains(keyword), User.level >= 0).all()
        context = {
            'users': the_users,
            'posts': the_posts
        }
        return flask.render_template('select.html', **context)
    else:
        return flask.redirect(flask.url_for('failed', info='查找失败...请输入关键字！'))


@app.route('/report/<user_id>/<flag>/<words_id>/')
@login_required
def report(user_id, flag, words_id):
    if flag == '1':
        the_post = Post.query.filter(Post.id == words_id).first()
        if the_post and the_post.author.id != 1:
            try:
                new_report = ReportP(user_id=user_id, post_id=words_id)
                db.session.add(new_report)
                db.session.commit()
                return flask.redirect(flask.url_for('succeeded', info='举报成功！感谢您维护了论坛的文明和谐！'))
            except Exception as e:
                db.session.rollback()
                return flask.redirect(flask.url_for('failed', info='举报失败...请稍后重新尝试！'))
        else:
            return flask.redirect(flask.url_for('failed', info='举报失败...举报出错！'))
    elif flag == '2':
        the_comment = Comment.query.filter(Comment.id == words_id).first()
        if the_comment and the_comment.author.id != 1:
            try:
                new_report = ReportC(user_id=user_id, comt_id=words_id)
                db.session.add(new_report)
                db.session.commit()
                return flask.redirect(flask.url_for('succeeded', info='举报成功！感谢您维护了论坛的文明和谐！'))
            except Exception as e:
                db.session.rollback()
                return flask.redirect(flask.url_for('failed', info='举报失败...请稍后重新尝试！'))
        else:
            return flask.redirect(flask.url_for('failed', info='举报失败...举报出错！'))
    else:
        return flask.redirect(flask.url_for('failed', info='举报失败...举报出错！'))


@app.route('/reportpage/')
@login_required
def reportpage():
    context = {
        'p': ReportP.query.filter(ReportP.handle == 0).all(),
        'c': ReportC.query.filter(ReportC.handle == 0).all()
    }
    return flask.render_template('reportpage.html', **context)


@app.route('/handle/<report_id>/<flag>/<solution>/')
@login_required
def dealwith(report_id, flag, solution):
    if flag == 1:
        the_report = ReportP.query.filter(ReportP.id == report_id)
        if the_report:
            if solution == '1':  # 不理会
                try:
                    the_report.handle = 1
                    the_report.handle_time = datetime.now
                    db.session.commit()
                    return flask.redirect(flask.url_for('succeeded', info='处理成功！您忽略了这条莫须有的举报！'))
                except Exception as e:
                    db.session.rollback()
                    return flask.redirect(flask.url_for('failed', info='处理失败...请稍后重新尝试！'))
            elif solution == '2':  # 删帖
                try:
                    the_report.handle = 2
                    the_report.article.status = 'blocked'
                    the_report.handle_time = datetime.now
                    db.session.commit()
                    return flask.redirect(flask.url_for('succeeded', info='处理成功！您已强制删贴！'))
                except Exception as e:
                    db.session.rollback()
                    return flask.redirect(flask.url_for('failed', info='处理失败...请稍后重新尝试！'))
            elif solution == '3':  # 删帖并封号
                try:
                    the_report.handle = 3
                    the_report.article.status = 'blocked'
                    the_report.article.atuhor.level = 0-the_report.article.atuhor.level
                    if the_report.article.atuhor.managed:
                        the_report.article.atuhor.managed.admin_id = 1
                    the_report.article.atuhor.is_admin = 'N'
                    the_report.article.atuhor.recognition = None
                    the_report.handle_time = datetime.now
                    db.session.commit()
                    return flask.redirect(flask.url_for('succeeded', info='处理成功！您已强制删贴并封号！'))
                except Exception as e:
                    db.session.rollback()
                    return flask.redirect(flask.url_for('failed', info='处理失败...请稍后重新尝试！'))
            else:
                return flask.redirect(flask.url_for('failed', info='处理失败...举报信息出错！'))
        else:
            return flask.redirect(flask.url_for('failed', info='处理失败...举报信息出错！'))
    elif flag == 2:
        the_report = ReportC.query.filter(ReportC.id == report_id)
        if the_report:
            if solution == '1':  # 不理会
                try:
                    the_report.handle = 1
                    the_report.handle_time = datetime.now
                    db.session.commit()
                    return flask.redirect(flask.url_for('succeeded', info='处理成功！您忽略了这条莫须有的举报！'))
                except Exception as e:
                    db.session.rollback()
                    return flask.redirect(flask.url_for('failed', info='处理失败...请稍后重新尝试！'))
            elif solution == '2':  # 删帖
                try:
                    the_report.handle = 2
                    the_report.comment.status = 'blocked'
                    the_report.handle_time = datetime.now
                    db.session.commit()
                    return flask.redirect(flask.url_for('succeeded', info='处理成功！您已强制删除评论！'))
                except Exception as e:
                    db.session.rollback()
                    return flask.redirect(flask.url_for('failed', info='处理失败...请稍后重新尝试！'))
            elif solution == '3':  # 删帖并封号
                try:
                    the_report.handle = 3
                    the_report.comment.status = 'blocked'
                    the_report.comment.atuhor.level = 0-the_report.article.atuhor.level
                    if the_report.comment.atuhor.managed:
                        the_report.comment.atuhor.managed.admin_id = 1
                    the_report.comment.atuhor.is_admin = 'N'
                    the_report.comment.atuhor.recognition = None
                    the_report.handle_time = datetime.now
                    db.session.commit()
                    return flask.redirect(flask.url_for('succeeded', info='处理成功！您已强制删除评论并封号！'))
                except Exception as e:
                    db.session.rollback()
                    return flask.redirect(flask.url_for('failed', info='处理失败...请稍后重新尝试！'))
            else:
                return flask.redirect(flask.url_for('failed', info='处理失败...举报信息出错！'))
        else:
            return flask.redirect(flask.url_for('failed', info='处理失败...举报信息出错！'))
    else:
        return flask.redirect(flask.url_for('failed', info='处理失败...举报信息出错！'))


@app.route('/succeeded/<info>/')
def succeeded(info):
    return flask.render_template('succeeded.html', info=info)


@app.route('/failed/<info>/')
def failed(info):
    return flask.render_template('failed.html', info=info)


@app.context_processor
def my_context_processor():
    user_id = flask.session.get('user_id')
    board_list = Board.query.all()
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            global_context = {
                'user': user,
                'board_list': board_list,
                'yearlist': range(-70, 1, 1),
                'monthlist': range(1, 13, 1),
                'daylist': range(1, 32, 1),
                'now': date.today()
            }
            return global_context
    else:
        global_context = {
            'board_list': board_list,
            'yearlist': range(-70, 1, 1),
            'monthlist': range(1, 13, 1),
            'daylist': range(1, 32, 1),
            'now': date.today()
        }
        return global_context


if __name__ == '__main__':
    app.run()
