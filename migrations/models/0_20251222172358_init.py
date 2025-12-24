from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "role" VARCHAR(20) NOT NULL DEFAULT 'user',
    "is_active" BOOL NOT NULL DEFAULT True,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "categories" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "description" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "ingredients" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "calories_per_100g" DOUBLE PRECISION NOT NULL,
    "protein_per_100g" DOUBLE PRECISION NOT NULL,
    "fat_per_100g" DOUBLE PRECISION NOT NULL,
    "carbs_per_100g" DOUBLE PRECISION NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "category_id" INT NOT NULL REFERENCES "categories" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "substitutes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "coefficient" DOUBLE PRECISION NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "original_ingredient_id" INT NOT NULL REFERENCES "ingredients" ("id") ON DELETE CASCADE,
    "substitute_ingredient_id" INT NOT NULL REFERENCES "ingredients" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_substitutes_origina_9aad19" UNIQUE ("original_ingredient_id", "substitute_ingredient_id")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmmtv2jwUx78KyqtO6qaOtdv0vANKNzYKE9BtWlVFJjHBamIzx1mLJr77YztXO5cBKx"
    "20eQfH5yT2z5fzP0l+Gx6xoeu/uvIhNf5r/DYw8CD/odiPGwZYLFKrMDAwdaVjwD2kBUx9"
    "RoHFuHEGXB9ykw19i6IFQwRzKw5cVxiJxR0RdlJTgNHPAJqMOJDNZUeub7gZYRveQz/+u7"
    "g1Zwi6ttJPZIt7S7vJlgtp62F2IR3F3aamRdzAw6nzYsnmBCfeCDNhdSCGFDAoLs9oILov"
    "ehcNMx5R2NPUJexiJsaGMxC4LDPcNRlYBAt+vDe+HKAj7vKy+fr03en7N29P33MX2ZPE8m"
    "4VDi8dexgoCQwmxkq2AwZCD4kx5SamTf7O0evMAS3Gl43RIPKu6xBjZP+UogfuTRdih835"
    "37OTCmRfW6POx9bo6OzkhRgJ4Us5XOCDqKUpmwTVlCL0AHI3QZgEHCK/1yfrAORepQRlm4"
    "pwAXz/jlDbnAN/vgnKXODDII0NKdP0NNsF1ObZ2RpQuVcpVNmmQqXE3Whnx/6Ph1AeJsaD"
    "QVxnYTbL12UztyyRb/Jchn4VYGwTTgvgkhSTjdNwTnngrngmG38rmhX02sNhX3Ta8/2frj"
    "T0JhrGq8t2l+97SZc7IQazOShlalEoRm0Clod6zlsY8mAxVTVSw2pHoa/iH3u67fkY7CF2"
    "l9FsVTCf9C6740nr8osC/rw16YqWprQuNevRW211JxdpfOtNPjbE38aP4aArCRKfOVTeMf"
    "Wb/DBEn0DAiInJnQnsTEaJrTEYZWKDhb3lxKqR9cT+04mVnRdKe3ab0YzCMAXW7R3guTbX"
    "QpqkzDff5DU93QIwcOSsCLail1Hh0eFT7BC6NAqKkqTtuKowsUIvBOvq5OCqk00rk0OuSn"
    "aiqrM9y3GcwPuSJaiFbYUzgvWIB3DVgdv9PlHO2pja0WXr+wvlvO0PBx9i9wzlTn/YrnXM"
    "U0x3oY7ZIN9lznXM72ojKJDk64Mo+OLzCLqgZC9FqayXXGg/J3sVr+DYmpUJu8r9GSgF2V"
    "9FVp7/tTmqBUAtAJ6RALCAK7WvuYDU5O1OnuaFS0DJSiyM1tjORPhen1pFOM+HV+1+t/Fl"
    "1O30xr3hQM1BslF9jDHqtvr6I0tKGER4O7RFwTXZiOwMsO2o6oE10eQcoNOtDwE9tKZaVw"
    "BPrwJQt0v4aMncSLhpUX9WcHsyjw8g4nLlU55lwaFDKEQO/gyXkmeP9wpgq0jAFTzx2z+O"
    "ZUUSN1Nwl1QF+jLhw+SDg+Eh02mNO63zrrFap/z0A17MIBYwrtBmlHh/V4OOk6sdFl5l42"
    "aRMPJMgeyyKM9AKSjKVWTlRXlmmh6+KL/mOQM5CAPXRMpDgvSu2YabuojfbRFvETibISue"
    "hfWFpxpXq85adT5t1VlwbG0mQMsv8Jy0aLEe2Bpq1SWeE9YKiV+Sb/9S7R/qSxFd75fvym"
    "Lp/8f1W7NN2FZtzk0Lq13K5hakyJobBZI5aqmUyyD1qV9f7dmxWKV8f0HqF356Uf4GKxNS"
    "f8icgBRbYwOIkfthAtzNe0CCWWHm+DQeDsrKryREA3mF+QCvbWSx44aLfHazn1grKIpRK0"
    "VB7nsg/dMfTe2LC7SLRNFjppfV/8Z9VAM="
)
