
drop:
	python -c "from app import db; db.drop_all()"

create: drop
	python -c "from app import db; db.create_all()"
