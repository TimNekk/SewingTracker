from dataclasses import dataclass


@dataclass
class Product:
    name: str
    article: int
    price: int
    in_stock: bool = True

    def __str__(self):
        return f"\"{self.name}\" (АРТ. {self.article})"
