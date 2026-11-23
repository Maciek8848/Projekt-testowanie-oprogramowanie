import database as db

db.conectTo("mock")
db.reset()

a = db.user.create("1", "1")
a = db.user.create("2", "1")

db.paper.create(1, "best paper")
db.review.create(1,2, "worst paper")

db.user.delete(2)

print(db.user.read())
print(db.paper.read())
print(db.review.read())

db.remove()