class Config(object):
    """
    Common configurations
    """
    # Name of the ZFS pool to use
    ZFS_POOL = 'zfs_pool_ubuntu'
    # Name of the dataset
    ZFS_DATASET = 'kvm-images'
    # Mountpoint for the dataset in use
    # TODO: add code to extract the mountpoint of the given pool and dataset
    #       if the ZFS_MOUNTPOINT is empty
    ZFS_MOUNTPOINT = '/kvm-images'
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

class TestingConfig(Config):
    """
    Testing configurations
    """
    
    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing' : TestingConfig
}