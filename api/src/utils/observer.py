class Subject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)


class Observer:
    def update(self, subject):
        pass


class ImportSubject(Subject):
    def __init__(self, initial_state=0, *args, **kwargs):
        super().__init__()
        self.state = initial_state

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        self.notify()


class ImportObserver(Observer):
    def update(self, subject):
        print("state changed to:", subject.get_state())


# Example usage
# subject = ImportSubject()
# observer = ImportObserver()
# subject.attach(observer)
# subject.set_state(1)
# Output：state changed to: 1
