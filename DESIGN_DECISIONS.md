# Design Decisions - Final Specifications

## Finalized Requirements (2025-12-09)

### Group Settings
- **Name Restrictions**: None
- **Name Max Length**: No limit
- **Name Uniqueness**: Not required (multiple groups can have same name)
- **Max Members**: 32 members per group

### Comments
- **Character Limit**: 1000 characters
- **Edit/Delete**: Not supported in MVP
- **Threading**: Not supported in MVP (flat comment list)

### Book Covers
- **Storage Strategy**: Hotlink from Open Library
- **Rationale**:
  - No storage costs
  - No bandwidth costs
  - Automatic updates if Open Library improves images
  - Fallback to placeholder if image unavailable

### User Avatars
- **Strategy**: Custom uploads (with Google avatar as initial default)
- **Storage**: Will need image hosting solution
- **Options for MVP**:
  - Railway/Render blob storage
  - Cloudinary free tier (25GB storage, 25GB bandwidth/month)
  - AWS S3 (minimal cost, ~$0.50/month)
- **Recommendation**: **Cloudinary free tier** (easiest integration, generous limits)
- **Format**: JPEG/PNG, max 2MB, auto-resize to 200x200px
- **Fallback**: Google avatar URL if no custom upload

### Beta Testing
- **Primary Testers**: Your book club
- **Initial Scale**: ~10-20 users expected
- **Test Book**: TBD (to be selected by your book club)

## Implementation Details

### Avatar Upload Flow
1. User logs in → Google avatar set as default
2. User can upload custom avatar from profile page
3. Image validated (size, format)
4. Uploaded to Cloudinary
5. URL stored in database
6. Avatar displayed throughout app

### Cloudinary Integration
```python
# Backend: cloudinary setup
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="your-cloud-name",
    api_key="your-api-key",
    api_secret="your-api-secret"
)

# Upload avatar
result = cloudinary.uploader.upload(
    file,
    folder="avatars",
    transformation=[
        {'width': 200, 'height': 200, 'crop': 'fill', 'gravity': 'face'}
    ]
)
avatar_url = result['secure_url']
```

### Group Member Limit Enforcement
```python
# Check before adding member
current_member_count = db.query(GroupMember).filter(
    GroupMember.group_id == group_id
).count()

if current_member_count >= 32:
    raise HTTPException(
        status_code=400,
        detail="Group is full (maximum 32 members)"
    )
```

### Comment Length Validation
```python
# Pydantic schema
class CommentCreate(BaseModel):
    content: str = Field(..., max_length=1000, min_length=1)
```

### Book Cover Handling
```python
# Open Library cover URL format
def get_book_cover_url(isbn=None, open_library_id=None, size='M'):
    """
    Get book cover from Open Library
    Size: S (small), M (medium), L (large)
    """
    if isbn:
        return f"https://covers.openlibrary.org/b/isbn/{isbn}-{size}.jpg"
    elif open_library_id:
        return f"https://covers.openlibrary.org/b/olid/{open_library_id}-{size}.jpg"
    else:
        return "/placeholder-book-cover.jpg"  # Fallback
```

## Updated Cost Analysis

### Hosting Costs (Annual)
- **Railway Backend**: $5/month = $60/year
- **Railway PostgreSQL**: $5/month = $60/year
- **Cloudinary**: $0 (free tier)
- **Domain**: $12/year
- **SSL**: $0 (included)
- **Total**: ~$132/year ✅ (under $200 budget)

### Cloudinary Free Tier Limits
- 25 GB storage (plenty for thousands of avatars)
- 25 GB monthly bandwidth
- 25,000 transformations/month
- Enough for MVP and beyond

## Database Schema Updates

### Users Table - Updated
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    avatar_url TEXT,  -- Google avatar initially, then custom upload
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Comments Table - Add Length Constraint
```sql
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL CHECK (LENGTH(content) <= 1000 AND LENGTH(content) >= 1),
    progress_page INTEGER NOT NULL,
    progress_total_pages INTEGER NOT NULL,
    progress_percentage DECIMAL(5,2) GENERATED ALWAYS AS ((progress_page::DECIMAL / progress_total_pages::DECIMAL) * 100) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Groups Table - Add Member Count Check
```sql
-- Add trigger to enforce member limit
CREATE OR REPLACE FUNCTION check_group_member_limit()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM group_members WHERE group_id = NEW.group_id) >= 32 THEN
        RAISE EXCEPTION 'Group is full (maximum 32 members)';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_member_limit
    BEFORE INSERT ON group_members
    FOR EACH ROW
    EXECUTE FUNCTION check_group_member_limit();
```

## UI/UX Updates

### Avatar Display Specifications
- **Size Variants**:
  - Tiny: 24×24px (comment metadata)
  - Small: 32×32px (member list)
  - Medium: 48×48px (comment cards)
  - Large: 96×96px (profile page)
  - XLarge: 200×200px (profile edit)

- **Style**:
  - Circular crop
  - 2px border in primary color for active users
  - Subtle shadow
  - Lazy loading for performance

### Group Full State UI
When group reaches 32 members:
- Invite link shows "Group Full" badge
- Join button disabled
- Message: "This group has reached its maximum capacity (32 members)"

### Comment Character Counter
- Show character count as user types: "256 / 1000"
- Turn red when approaching limit (900+)
- Disable submit when at 0 or over 1000

## Development Priorities

### Phase 1: Core Backend (Week 1-2)
1. ✅ Database schema
2. ✅ User authentication (Google OAuth)
3. ✅ Group CRUD operations
4. ✅ Book search integration
5. ✅ Comment visibility logic

### Phase 2: Avatar System (Week 3)
1. Cloudinary integration
2. Avatar upload endpoint
3. Image validation
4. Avatar display throughout app

### Phase 3: Frontend (Week 4-6)
1. Authentication flow
2. Group management UI
3. Comment feed with avatars
4. Progress tracking
5. Avatar upload UI

### Phase 4: Polish & Testing (Week 7-8)
1. Mobile responsiveness
2. Performance optimization
3. Testing with your book club
4. Bug fixes

### Phase 5: Deployment (Week 9)
1. Railway deployment
2. Domain setup
3. Cloudinary production config
4. Launch with book club

## Testing Strategy with Your Book Club

### Week 1-2: Internal Testing (You + 1-2 others)
- Test basic flows
- Fix critical bugs
- Refine UX

### Week 3-4: Book Club Beta (Full group)
- Select a book everyone's reading
- Use platform exclusively for that book
- Gather feedback
- Iterate quickly

### Success Metrics
- Zero spoilers reported
- All members can successfully post and see comments
- Comments filter correctly based on progress
- No performance issues with 10-20 concurrent users

## Open Items

### Before Development Starts
- [ ] Create Google OAuth credentials
- [ ] Set up Cloudinary account
- [ ] Choose PostgreSQL hosting (Railway or local dev)
- [ ] Decide on book for beta test

### Before Deployment
- [ ] Choose domain name
- [ ] Purchase domain
- [ ] Set up Railway account
- [ ] Configure production environment variables

## Notes for Implementation

### Avatar Upload Security
- Validate file type (only JPEG, PNG)
- Validate file size (max 2MB)
- Scan for malware (if concerned)
- Rate limit uploads (max 5 per hour)
- Sanitize filenames

### Book Cover Fallback Strategy
1. Try ISBN cover from Open Library
2. If 404, try Open Library ID
3. If 404, use placeholder image
4. Cache cover URLs to avoid repeated checks

### Group Name Display
Since names don't need to be unique:
- Display group name + creation date in lists
- Show "Created by [Name]" to help distinguish
- Use group ID in URLs, not name

### Comment Pagination
For large discussions:
- Load 50 comments initially
- Infinite scroll or "Load More" button
- Comments sorted chronologically (oldest first)
- Anchor link to jump to your current progress

---

**All design decisions finalized and ready for implementation!**

**Status**: ✅ Complete - Ready to Build
**Last Updated**: 2025-12-09
