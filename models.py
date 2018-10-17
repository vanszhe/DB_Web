from exts import db
from datetime import datetime, date


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum("M", "N", "F"), nullable=False, default='N')
    birthday = db.Column(db.Date)
    recognition = db.Column(db.String(20))
    is_admin = db.Column(db.Enum("Y", "N"), nullable=False, default='N')
    level = db.Column(db.Integer, nullable=False, default=1)
    exp = db.Column(db.Integer, nullable=False, default=0)
    pic = db.Column(db.String(100), nullable=False, default='images/userdefault.png')
    balance = db.Column(db.Integer, nullable=False, default=0)


class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)

    admin = db.relationship('User', backref=db.backref('managed'))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_day = db.Column(db.Date, nullable=False, default=date.today())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'), nullable=False)
    com_num = db.Column(db.Integer, nullable=False, default=0)
    favor_num = db.Column(db.Integer, nullable=False, default=0)
    reward = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Enum("reviewing", "normal", "blocked", "hot"), nullable=False, default="reviewing")

    author = db.relationship('User', backref=db.backref('articles'))
    board = db.relationship('Board', backref=db.backref('articles'))


# 评论表comments_c
# 评论总id 唯一标识
# 评论者id，外键与users表id属性连接
# 评论内容，
# 评论所属的帖子，外键与posts表id属性连接
# 评论所属帖子的楼层号
# 评论的父评论，对应楼层号，可为null，为null表示不是某一条评论的评论
# 评论日期
# 获赞数，整数可正可负
# 状态，包括：正常、隐藏、热门
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    parent = db.Column(db.Integer)
    com_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    like_num = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Enum("normal", "blocked", "hot"), nullable=False, default="normal")

    author = db.relationship('User', backref=db.backref('comments'))
    article = db.relationship('Post', backref=db.backref('comments'))


# 收藏记录
# 总id号
# 收藏者id 外键链接user
# 被收藏帖子id 外键链接post
class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    users = db.relationship('User', backref=db.backref('favorite_posts'))
    article = db.relationship('Post', backref=db.backref('be_favored_by'))


# 举报记录
# 总id号
# 举报人id 外键users
# 举报类型 1、2
# 举报帖子id 外键posts
# 举报评论id 外键comments
# 处理状态 1、2、3、4
# 举报时间
# 处理时间
class ReportP(db.Model):
    __tablename__ = 'reports_p'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    handle = db.Column(db.Integer, nullable=False, default=0)
    report_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    handle_time = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('reports_p'))
    article = db.relationship('Post', backref=db.backref('reported'))


class ReportC(db.Model):
    __tablename__ = 'reports_c'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comt_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    handle = db.Column(db.Integer, nullable=False, default=0)
    report_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    handle_time = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('reports_c'))
    comment = db.relationship('Comment', backref=db.backref('reported'))
