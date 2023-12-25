from wtforms import Form
from wtforms.fields import simple


class FormMeta(type):
    def __init__(cls, name, bases, attrs):
        type.__init__(cls, name, bases, attrs)
        cls._unbound_fields = None
        cls._wtforms_meta = None

    def __call__(cls, *args, **kwargs):
        """
        Construct a new `Form` instance.

        Creates the `_unbound_fields` list and the internal `_wtforms_meta`
        subclass of the class Meta in order to allow a proper inheritance
        hierarchy.
        """
        if cls._unbound_fields is None:
            fields = []
            for name in dir(cls):
                if not name.startswith('_'):
                    unbound_field = getattr(cls, name)
                    if hasattr(unbound_field, '_formfield'):
                        fields.append((name, unbound_field))
            # We keep the name as the second element of the sort
            # to ensure a stable sort.
            fields.sort(key=lambda x: (x[1].creation_counter, x[0]))
            cls._unbound_fields = fields

        # Create a subclass of the 'class Meta' using all the ancestors.
        if cls._wtforms_meta is None:
            bases = []
            for mro_class in cls.__mro__:
                if 'Meta' in mro_class.__dict__:
                    bases.append(mro_class.Meta)
            cls._wtforms_meta = type('Meta', tuple(bases), {})
        return type.__call__(cls, *args, **kwargs)


def with_metaclass(meta, base=object):
    #     FormMeta("NewBase", (BaseForm,), {} )
    #         type("NewBase", (BaseForm,), {} )
    return meta("NewBase", (base,), {})

"""
class NewBase(BaseForm,metaclass=FormMeta):
    pass


class Form(  NewBase):
"""
class Form(  with_metaclass(FormMeta, BaseForm)  ):
    pass


# LoginForm其实是由 FormMeta 创建的。
#   1. 创建类时，会执行  FormMeta 的 __new__ 和 __init__，内部在类中添加了两个类变量 _unbound_fields 和 _wtforms_meta
class LoginForm(Form):
    name = simple.StringField(label='用户名', render_kw={'class': 'form-control'})
    pwd = simple.PasswordField(label='密码', render_kw={'class': 'form-control'})


#   2.根据LoginForm类去创建对象。   FormMeta.__call__ 方法   -> LoginForm中的new去创建对象,init去初始化对象。

form = LoginForm()
print(form.name)  # 类变量
print(form.pwd)  # 类变量

# 问题1：此时LoginForm是由 type or FormMeta创建？
"""
类中metaclass，自己类由于metaclass定义的类来创建。
类继承某个类，父类metaclass，自己类由于metaclass定义的类来创建。
"""

