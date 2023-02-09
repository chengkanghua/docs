from functools import lru_cache
from host.models import PkeyModel


class PkeyManager(object):
    keys = ('public_key', 'private_key',)

    # 由于我们可能经常会执行这个get操作，所以我们使用了django的缓存机制，对方法的结果进行缓存，
    # 第二次调用 get()方法 时，并没有真正执行方法，而是直接返回缓存的结果，
    # 参数maxsize为最多缓存的次数，如果为None，则无限制，设置为2n时，性能最佳
    @classmethod
    @lru_cache(maxsize=64)
    def get(cls, name):
        info = PkeyModel.objects.filter(name=name).first()
        if not info:
            raise KeyError(f'没有这个 {name!r} 秘钥对')

        # 以元组格式，返回公私钥
        return (info.private, info.public)

    @classmethod
    def set(cls, name, private_key, public_key, description=None):
        """保存公私钥"""
        PkeyModel.objects.update_or_create(name=name, defaults={
            'private': private_key,
            'public': public_key,
            'description': description
        })
