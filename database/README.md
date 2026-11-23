funkcja `conectTo()` zmiena do jakiego pliku się podłanczacie \
czyli `conectTo(mock)` będzie odnosiła się do pliku o nazwie mock

`reset()` tworzy/resetuje obecnie podłączoną baze na bazie db_init.sql

`remove()` usuwa plit obecne podłączonej bazy

wszystkie trzy moduły mają:
- create
- update
- read
- delete

funkcja `readId` zwraca liste id np. paper.readId(1) zwruci liste id wszystkich paperów których autorem jest urzytkownik o id 1