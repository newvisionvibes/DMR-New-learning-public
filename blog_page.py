"""
Streamlit Blog Module for Flo.io ETF RS Analyzer
Geopolitical Blog Tab - Integrated with existing auth system
Author: Flo.io Team
Version: 1.0
"""

import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
import pandas as pd

# ==================== CONFIGURATION ====================

BLOG_DATA_PATH = "data/blog_posts.json"
BLOG_ARCHIVE_PATH = "data/blog_archive"

# Ensure data directory exists
Path("data").mkdir(exist_ok=True)
Path(BLOG_ARCHIVE_PATH).mkdir(exist_ok=True)

# Geopolitical tags for blog posts
BLOG_TAGS = [
    "Geopolitical",
    "India",
    "Global",
    "Trade",
    "Security",
    "Market Impact",
    "Currency",
    "Commodities",
    "Energy",
    "Tech",
]

# ==================== DATABASE FUNCTIONS ====================

def load_blog_posts():
    """Load all blog posts from JSON"""
    if not os.path.exists(BLOG_DATA_PATH):
        return []
    try:
        with open(BLOG_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_blog_posts(posts):
    """Save blog posts to JSON"""
    os.makedirs(os.path.dirname(BLOG_DATA_PATH), exist_ok=True)
    with open(BLOG_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

def add_blog_post(title, content, tags, author):
    """Add new blog post"""
    posts = load_blog_posts()
    new_post = {
        "id": int(datetime.now().timestamp() * 1000),
        "title": title,
        "content": content,
        "author": author,
        "date": datetime.now().isoformat(),
        "tags": tags,
        "comments": [],
        "likes": [],
        "views": 0,
    }
    posts.insert(0, new_post)
    save_blog_posts(posts)
    return new_post

def add_comment(post_id, comment_text, author):
    """Add comment to a post"""
    posts = load_blog_posts()
    for post in posts:
        if post["id"] == post_id:
            new_comment = {
                "id": int(datetime.now().timestamp() * 1000),
                "author": author,
                "text": comment_text,
                "date": datetime.now().isoformat(),
            }
            post["comments"].append(new_comment)
            save_blog_posts(posts)
            return True
    return False

def delete_comment(post_id, comment_id, user_role, current_user):
    """Delete comment (owner or admin only)"""
    posts = load_blog_posts()
    for post in posts:
        if post["id"] == post_id:
            for comment in post["comments"]:
                if comment["id"] == comment_id:
                    if user_role == "admin" or comment["author"] == current_user:
                        post["comments"].remove(comment)
                        save_blog_posts(posts)
                        return True
    return False

def toggle_like(post_id, username):
    """Toggle like on a post"""
    posts = load_blog_posts()
    for post in posts:
        if post["id"] == post_id:
            if username in post["likes"]:
                post["likes"].remove(username)
                liked = False
            else:
                post["likes"].append(username)
                liked = True
            save_blog_posts(posts)
            return liked, len(post["likes"])
    return False, 0

def increment_views(post_id):
    """Increment view count"""
    posts = load_blog_posts()
    for post in posts:
        if post["id"] == post_id:
            post["views"] = post.get("views", 0) + 1
            save_blog_posts(posts)
            break

def delete_post(post_id):
    """Delete a post (admin only)"""
    posts = load_blog_posts()
    posts = [p for p in posts if p["id"] != post_id]
    save_blog_posts(posts)

def search_posts(query, tag_filter=None):
    """Search posts by keyword or tag"""
    posts = load_blog_posts()
    results = []
    
    query_lower = query.lower()
    for post in posts:
        # Filter by query
        if query and (
            query_lower in post["title"].lower()
            or query_lower in post["content"].lower()
        ):
            results.append(post)
        # Filter by tag
        elif tag_filter and tag_filter in post.get("tags", []):
            results.append(post)
        # No filters - include all
        elif not query and not tag_filter:
            results.append(post)
    
    return results

def get_blog_stats(user_role=None):
    """Get blog statistics"""
    posts = load_blog_posts()
    
    stats = {
        "total_posts": len(posts),
        "total_comments": sum(len(p.get("comments", [])) for p in posts),
        "total_views": sum(p.get("views", 0) for p in posts),
        "total_likes": sum(len(p.get("likes", [])) for p in posts),
    }
    
    # Tag distribution
    tag_count = {}
    for post in posts:
        for tag in post.get("tags", []):
            tag_count[tag] = tag_count.get(tag, 0) + 1
    stats["tags"] = tag_count
    
    # Top posts
    stats["top_posts"] = sorted(posts, key=lambda x: x.get("views", 0), reverse=True)[:5]
    
    return stats

# ==================== UI COMPONENTS ====================

def render_blog_header():
    """Render blog page header"""
    st.markdown("# 📰 Geopolitical Blog")
    st.markdown(
        "Stay updated with latest geopolitical trends and their market impact. "
        "Insights from industry experts to help guide your investment decisions."
    )

def render_post_card(post, user_info, show_delete=False):
    """Render a single blog post card"""
    with st.container():
        # Post Header
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"### {post['title']}")
        
        with col2:
            if show_delete:
                if st.button("🗑️ Delete", key=f"del_{post['id']}"):
                    delete_post(post["id"])
                    st.success("Post deleted!")
                    st.rerun()
        
        with col3:
            st.caption(f"👁️ {post.get('views', 0)} views")
        
        # Post Meta
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.caption(f"✍️ By **{post['author']}**")
        with col2:
            post_date = datetime.fromisoformat(post["date"])
            st.caption(f"📅 {post_date.strftime('%d %b %Y, %H:%M')}")
        with col3:
            st.caption(f"💬 {len(post.get('comments', []))} comments")
        with col4:
            st.caption(f"❤️ {len(post.get('likes', []))} likes")
        
        # Tags
        if post.get("tags"):
            tag_cols = st.columns(len(post["tags"]))
            for i, tag in enumerate(post["tags"]):
                with tag_cols[i]:
                    st.write(f"🏷️ `{tag}`")
        
        # Content
        st.markdown(post["content"])
        
        # Like Button
        if user_info:
            col1, col2, col3 = st.columns([1, 2, 2])
            with col1:
                is_liked = user_info["username"] in post.get("likes", [])
                like_text = "❤️ Unlike" if is_liked else "🤍 Like"
                if st.button(like_text, key=f"like_{post['id']}"):
                    toggle_like(post["id"], user_info["username"])
                    st.rerun()
        
        st.divider()
        
        # Comments Section
        st.markdown("#### Comments")
        
        # Display existing comments
        for comment in post.get("comments", []):
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{comment['author']}** • {datetime.fromisoformat(comment['date']).strftime('%d %b, %H:%M')}")
                    st.write(comment["text"])
                
                with col2:
                    if user_info and (
                        user_info["role"] == "admin"
                        or user_info["username"] == comment["author"]
                    ):
                        if st.button("🗑️", key=f"del_comment_{comment['id']}"):
                            delete_comment(
                                post["id"],
                                comment["id"],
                                user_info["role"],
                                user_info["username"],
                            )
                            st.success("Comment deleted!")
                            st.rerun()
                
                st.caption("---")
        
        # Add Comment Form
        if user_info:
            comment_text = st.text_area(
                "Add your comment...",
                key=f"comment_input_{post['id']}",
                height=80,
            )
            if st.button("Post Comment", key=f"submit_comment_{post['id']}"):
                if comment_text.strip():
                    add_comment(post["id"], comment_text, user_info["username"])
                    st.success("Comment posted!")
                    st.rerun()
                else:
                    st.warning("Please write a comment")
        else:
            st.info("👤 Login to comment on posts")
        
        st.markdown("---")

# ==================== MAIN BLOG PAGE ====================

def blog_page(user_info):
    """Main blog page with all functionality"""
    
    render_blog_header()
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📖 Blog Feed", "🔍 Search & Filter", "📊 Analytics"])
    
    # ==================== TAB 1: BLOG FEED ====================
    with tab1:
        # Admin: Create Post Section
        if user_info and user_info.get("role") == "admin":
            st.markdown("### ✍️ Create New Post")
            with st.form("create_post_form"):
                post_title = st.text_input("Post Title", placeholder="e.g., India-US Trade Deal 2025")
                post_content = st.text_area(
                    "Post Content",
                    placeholder="Share your geopolitical analysis...",
                    height=200,
                )
                post_tags = st.multiselect(
                    "Tags",
                    BLOG_TAGS,
                    default=["Geopolitical"],
                )
                
                submitted = st.form_submit_button("📤 Post Update")
                if submitted:
                    if post_title and post_content:
                        add_blog_post(
                            post_title,
                            post_content,
                            post_tags,
                            user_info["username"],
                        )
                        st.success("✅ Post published successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill in title and content")
            
            st.divider()
        
        # Display Blog Posts
        st.markdown("### Recent Posts")
        posts = load_blog_posts()
        
        if not posts:
            st.info("📭 No blog posts yet. Check back soon!")
        else:
            for post in posts:
                # Track view
                increment_views(post["id"])
                render_post_card(
                    post,
                    user_info,
                    show_delete=user_info and user_info.get("role") == "admin",
                )
    
    # ==================== TAB 2: SEARCH & FILTER ====================
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            search_query = st.text_input(
                "🔍 Search posts by keyword",
                placeholder="e.g., India, trade, security...",
            )
        
        with col2:
            tag_filter = st.selectbox(
                "🏷️ Filter by tag",
                options=[""] + BLOG_TAGS,
            )
        
        # Search
        if search_query or tag_filter:
            results = search_posts(search_query, tag_filter if tag_filter else None)
            st.markdown(f"### Search Results ({len(results)} posts)")
            
            if results:
                for post in results:
                    render_post_card(
                        post,
                        user_info,
                        show_delete=user_info and user_info.get("role") == "admin",
                    )
            else:
                st.info("No posts matching your search criteria")
        else:
            st.info("💡 Use search or tag filter to find posts")
    
    # ==================== TAB 3: ANALYTICS ====================
    with tab3:
        if user_info and user_info.get("role") == "admin":
            st.markdown("### 📊 Blog Analytics Dashboard")
            
            stats = get_blog_stats()
            
            # Stats Cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Posts", stats["total_posts"])
            with col2:
                st.metric("Total Comments", stats["total_comments"])
            with col3:
                st.metric("Total Views", stats["total_views"])
            with col4:
                st.metric("Total Likes", stats["total_likes"])
            
            st.divider()
            
            # Tag Distribution
            if stats["tags"]:
                st.markdown("#### 🏷️ Posts by Tag")
                tag_df = pd.DataFrame(
                    list(stats["tags"].items()),
                    columns=["Tag", "Count"],
                ).sort_values("Count", ascending=False)
                
                st.bar_chart(tag_df.set_index("Tag"))
            
            # Top Posts
            if stats["top_posts"]:
                st.markdown("#### 🏆 Top Posts by Views")
                top_posts_data = [
                    {
                        "Title": p["title"],
                        "Views": p.get("views", 0),
                        "Comments": len(p.get("comments", [])),
                        "Likes": len(p.get("likes", [])),
                    }
                    for p in stats["top_posts"]
                ]
                st.dataframe(
                    pd.DataFrame(top_posts_data),
                    use_container_width=True,
                )
        else:
            st.warning("⚠️ Admin access required to view analytics")

# ==================== EXPORT FUNCTION ====================

def get_blog_module():
    """Export blog page function for integration with main app"""
    return blog_page
