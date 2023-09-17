from tqdm import tqdm


class Progress:
    pbar: tqdm = None
    counter: int = 0

    @classmethod
    def set_pbar(cls, pbar: tqdm):
        cls.pbar = pbar

    @classmethod
    def update(cls):
        cls.counter += 1
        if cls.pbar is not None:
            cls.pbar.update()

    @classmethod
    def get_counter(cls):
        return cls.counter

    @classmethod
    def reset_counter(cls):
        cls.counter = 0