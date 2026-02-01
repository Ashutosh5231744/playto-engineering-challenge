 
---

# 📄 2️⃣ `EXPLAINER.md` (CODE)

👉 **EXPLAINER.md open karo**  
👉 **Poora paste** karo ⬇️  
👉 **Ctrl + S**

```md
# Playto Engineering Challenge – Explainer

## 1. Nested Comment Tree Design

Threaded comments are implemented using a self-referential foreign key.

Each comment has:
- A reference to the post
- A reference to the author
- A `parent` field pointing to another comment (nullable)

This design allows unlimited nesting of replies.

### Avoiding N+1 Queries
To efficiently load nested comments, the feed query uses:
- `select_related` for post authors
- `prefetch_related` for comments and their replies

This ensures minimal database queries even for deep comment trees.

---

## 2. Karma & Leaderboard Logic (Last 24 Hours)

Karma is not stored directly on the User model.
Each Like acts as a karma transaction.

### Rules:
- Like on Post → +5 Karma
- Like on Comment → +1 Karma
- Only likes from the last 24 hours are counted

### Leaderboard Query (Django ORM):

```python
User.objects
.filter(like__created_at__gte=last_24_hours)
.annotate(
    karma=Sum(
        Case(
            When(like__like_type='post', then=5),
            When(like__like_type='comment', then=1),
            default=0,
            output_field=IntegerField()
        )
    )
)
.order_by('-karma')[:5]
