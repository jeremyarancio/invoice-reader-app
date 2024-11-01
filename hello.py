from pydantic import BaseModel


class Model(BaseModel):
    a: str
    b: str


if __name__ == "__main__":
    print("hello")
    model = Model(a="hello",b="world")
    print(model)