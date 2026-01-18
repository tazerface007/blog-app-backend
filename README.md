# Blog App Backend


## ***DB Migrations***

```bash
flask db init
flask db migrate
flask db upgrade
```


## README


## ***Core Entities (High Level)***

**Main Tables**

1. **AdminUser**: for login (single user)
2. **Post** - blog content + SEO + draft/publish
3. **Category** - optional but useful
4. **Tag**
5. **PostTag** - many-to-many
6. **Comment** - reader comments
7. **CommentOTP** - OTP verification
8. **Media** - images, tables, files


## ***Database Schema (SQLAlchemy)***