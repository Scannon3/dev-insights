dev insights stores data from different github api endpoints... users,repositories,events,repo languages and uses it to derive insights such as ranked list of languages/bytes used, sorted events by date and filterable by type, and repo information ordered by date

users- holds unique id pk,login,users name, and number of repos 

repositories- holds unique id, user_id(foreign key linking to users),name of repo,primary language of repo, and when it was pushed 

repository_languages-holds repository_id(foreign key links to repository),language and bytes used for each.

events- holds event id,type of event,the repo_id,and repo_name. no foreign key necessary as we want to collect all events even if they dont belong to a repo in the db

users,repositories,language use upsert as we want the current state for these tables and events uses insert or ignore because we do not want to update events as they do not change(immutable). Both these work to prevent duplicates, just handled differently.

its important that repo_languages uses a composite key because a surrogate key will lead to duplicates whenever the bytes are updated as the updated bytes row will have a new id and there will be no conflict

Event.repo_id is only a soft reference because we want to store all events even if they dont correspond to a repo in the database. if this were a hard foreign key and we tried to store an event referencing a repo not in the db it will be rejected

datetimes stored as real datetime objects to prevent sloppy date strings/corrupted data as dates are important for the derived data and there  are too many different formats for dates, this makes it consistent and easier to make computations/operations based on date

started with sqlite to quickly get set up and built using ORM(SQLAlchemy) to make it easier to transition to postgres at a later time. writing raw sql instead wopuld have meant alll the queries would have to be redone when switching as different databases have slightly different syntax for sql

foreign key repositories.user_id maps back to users.id. one user can have many repositories.

foreign key repository_languages.repository_id maps to repositories_id. many languages to one repository

trade offs:

soft reference on event.repo_id gives up referential integrity, databsae no longer guarentees that an events repo_id points to a real stored repo, so some events dangle

SQLite+ORM - the swap to postgres will require insert functions to change to postgres equivlent

currente state upsert(do update) gives up history because repos are overwritten, so only latest snapshot is held

