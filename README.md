# SecretSharing-to-image
面向图像的秘密共享，采用shamir门限法进行秘密共享，再通过拉格朗日插值法进行解密恢复原图像。选取素数p=257，将所有255和256改为255并在数据尾部加上一个该数值对255的余数值数据。