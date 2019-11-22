class BaseDataAccess:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def create_item(self, **kwargs):
        model_data = self.model(**kwargs)
        self.db.session.add(model_data)
        self.db.session.commit()

    def edit_item(self, id, **kwargs):
        self.db.session.query(self.model).filter(self.model.id == id).update(kwargs)
        self.db.session.commit()

    def list_item(self, **kwargs):
        pass

    def verify_qualified_item(self, **kwargs):
        existed_item = self.model.query.filter_by(**kwargs).first()
        if existed_item is None:
            return True
        return False