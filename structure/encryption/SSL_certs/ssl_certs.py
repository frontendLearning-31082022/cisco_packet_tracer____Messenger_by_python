class Linux:
    nonne=0
    # openssl genrsa -aes256 -out priv.pem 4096
    # cat priv.pem
    # openssl rsa -text -in priv.pem
    # openssl rsa -in priv.pem -pubout -out pub.pem
    #
    # openssl req -new -key priv.pem -out cert.csr
    # openssl req -text -in cert.csr -noout
    # openssl x509 -req -days 365 -in cert.csr -signkey priv.pem -out cert.crt

class Windows:
    noeee=0

class Pytthon:

    @staticmethod
    def gen_priv_and_public(path_priv,path_pub):
        from Crypto.PublicKey import RSA
        key=RSA.generate(2048)
        privite_string=key.exportKey()
        with open(path_priv,"w") as private_file:
            print("{}".format(privite_string.decode()), file=private_file)
        public_string = key.publickey().exportKey()
        with open(path_pub, "w") as public_file:
            print("{}".format(public_string.decode()), file=public_file)

if __name__ == '__main__':
    Pytthon.gen_priv_and_public("out/private.pem",
                                "out/public.pem")