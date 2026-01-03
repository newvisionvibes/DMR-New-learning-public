"""
🎨 BLOG PAGE - Frontend UI for Blog System
==========================================

Streamlit UI for blog display and management:
- Admin: Create, edit, delete, publish posts
- Subscriber: Read published posts, filter by frequency
- Role-based access control
- Beautiful markdown rendering
- Frequency-based filtering

Production-ready Streamlit component.
"""

import streamlit as st
from modules.blog_manager import BlogManager, get_blog_manager

from datetime import datetime
import pytz


def blogpage():
    """
    Main blog page component.
    Shows different UI based on user role (admin vs subscriber).
    Call this in your Streamlit app: blogpage()
    """
    
    # Get current user role from session state
    user_role = st.session_state.get("user_role", "subscriber")
    username = st.session_state.get("username", "Unknown")
    
    if user_role == "admin":
        _admin_blog_interface(username)
    else:
        _subscriber_blog_interface()


# ============================================================================
# ADMIN INTERFACE
# ============================================================================

def _admin_blog_interface(admin_username: str) -> None:
    """Admin blog management interface"""
    
    st.subheader("✏️ Blog Management (Admin)")
    
    manager = get_blog_manager()
    stats = manager.get_statistics()
    
    # Show statistics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Posts", stats['total_posts'])
    with col2:
        st.metric("Published", stats['published'])
    with col3:
        st.metric("Drafts", stats['drafts'])
    with col4:
        st.metric("Categories", stats['categories'])
    with col5:
        st.metric("Weekly Posts", stats['weekly'])
    
    st.divider()
    
    # Admin tabs
    admin_tabs = st.tabs([
        "📝 Create Post",
        "📋 Manage Posts",
        "👁️ Preview",
        "⚙️ Categories"
    ])
    
    # Tab 1: Create Post
    with admin_tabs[0]:
        _create_post_form(manager, admin_username)
    
    # Tab 2: Manage Posts
    with admin_tabs[1]:
        _manage_posts_view(manager)
    
    # Tab 3: Preview Subscriber View
    with admin_tabs[2]:
        _preview_subscriber_view(manager)
    
    # Tab 4: Category Management
    with admin_tabs[3]:
        _category_management(manager)


def _create_post_form(manager: BlogManager, author: str) -> None:
    """Form for creating new blog posts"""
    
    st.write("Create a new blog post")
    
    with st.form("create_post_form"):
        title = st.text_input(
            "Post Title",
            placeholder="e.g., Weekly Sector Performance Analysis"
        )
        
        content = st.text_area(
            "Post Content",
            placeholder="Write your post here... (Markdown supported)",
            height=200
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category = st.selectbox(
                "Category",
                options=manager.get_categories()
            )
        
        with col2:
            frequency = st.selectbox(
                "Frequency",
                options=["daily", "weekly", "monthly"]
            )
        
        with col3:
            status = st.selectbox(
                "Status",
                options=["draft", "published"]
            )
        
        submitted = st.form_submit_button("📝 Create Post", width="stretch")
        
        if submitted:
            success, message, post_id = manager.create_post(
                title=title,
                content=content,
                author=author,
                frequency=frequency,
                category=category,
                status=status
            )
            
            if success:
                st.success(message)
                st.balloons()
            else:
                st.error(message)


def _manage_posts_view(manager: BlogManager) -> None:
    """View and edit existing posts"""
    
    st.write("Manage all posts (published and drafts)")
    
    all_posts = manager.get_all_posts()
    
    if not all_posts:
        st.info("No posts yet. Create your first post in the 'Create Post' tab.")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_status = st.multiselect(
            "Filter by status",
            options=["draft", "published"],
            default=["draft", "published"]
        )
    with col2:
        filter_category = st.multiselect(
            "Filter by category",
            options=manager.get_categories(),
            default=manager.get_categories()
        )
    
    # Filter posts
    filtered_posts = [
        p for p in all_posts
        if p.get('status') in filter_status and p.get('category') in filter_category
    ]
    
    if not filtered_posts:
        st.warning("No posts match the selected filters.")
        return
    
    # Display posts
    for idx, post in enumerate(filtered_posts):
        with st.expander(f"📄 {post['title']} ({post['status'].upper()})"):
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.caption(f"**Author:** {post['author']} | **Category:** {post['category']}")
            with col2:
                st.caption(f"**Frequency:** {post['frequency']}")
            with col3:
                status_color = "🟢" if post['status'] == "published" else "🟡"
                st.caption(f"{status_color} {post['status'].title()}")
            
            st.caption(f"Created: {post['created_at']} | Updated: {post['updated_at']}")
            
            st.divider()
            
            # Show content preview
            st.markdown("**Content:**")
            st.markdown(post['content'][:300] + "..." if len(post['content']) > 300 else post['content'])
            
            st.divider()
            
            # Edit and delete buttons
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                if st.button("✏️ Edit", key=f"edit_{post['id']}"):
                    st.session_state[f"editing_{post['id']}"] = True
            
            with col2:
                # Toggle publish/draft
                new_status = "draft" if post['status'] == "published" else "published"
                if st.button(f"📌 {new_status.title()}", key=f"toggle_{post['id']}"):
                    success, msg = manager.update_post(post['id'], status=new_status)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{post['id']}", help="Permanently delete this post"):
                    success, msg = manager.delete_post(post['id'])
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            
            # Edit form (shown if editing)
            if st.session_state.get(f"editing_{post['id']}", False):
                st.divider()
                st.write("**Edit Post:**")
                
                with st.form(f"edit_post_{post['id']}"):
                    new_title = st.text_input("Title", value=post['title'])
                    new_content = st.text_area("Content", value=post['content'], height=150)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_category = st.selectbox(
                            "Category",
                            options=manager.get_categories(),
                            index=manager.get_categories().index(post['category'])
                        )
                    with col2:
                        new_frequency = st.selectbox(
                            "Frequency",
                            options=["daily", "weekly", "monthly"],
                            index=["daily", "weekly", "monthly"].index(post['frequency'])
                        )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submitted = st.form_submit_button("💾 Save Changes", width="stretch")
                    with col2:
                        if st.form_submit_button("❌ Cancel", width="stretch"):
                            st.session_state[f"editing_{post['id']}"] = False
                            st.rerun()
                    
                    if submitted:
                        success, msg = manager.update_post(
                            post['id'],
                            title=new_title,
                            content=new_content,
                            category=new_category,
                            frequency=new_frequency
                        )
                        if success:
                            st.success(msg)
                            st.session_state[f"editing_{post['id']}"] = False
                            st.rerun()
                        else:
                            st.error(msg)


def _preview_subscriber_view(manager: BlogManager) -> None:
    """Preview what subscribers will see"""
    
    st.write("Preview the subscriber blog feed")
    
    published_posts = manager.get_published_posts()
    
    if not published_posts:
        st.info("No published posts yet. Publish a post first to see the subscriber view.")
        return
    
    st.success(f"✅ {len(published_posts)} published posts visible to subscribers")
    
    st.divider()
    
    # Show as subscriber would see it
    for post in published_posts:
        with st.container(border=True):
            st.markdown(f"### {post['title']}")
            st.caption(f"📅 {post['created_at']} | ✍️ By {post['author']} | 🏷️ {post['category']}")
            st.markdown(post['content'])
            st.caption(f"Frequency: **{post['frequency'].title()}**")


def _category_management(manager: BlogManager) -> None:
    """Manage blog categories"""
    
    st.write("Manage blog categories")
    
    categories = manager.get_categories()
    
    st.subheader("Current Categories")
    col1, col2 = st.columns([3, 1])
    
    for cat in categories:
        with col1:
            st.write(f"• {cat}")
        with col2:
            if st.button("🗑️", key=f"del_cat_{cat}", help=f"Delete {cat}"):
                success, msg = manager.delete_category(cat)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    
    st.divider()
    
    st.subheader("Add New Category")
    with st.form("add_category_form"):
        new_category = st.text_input("Category name", placeholder="e.g., Chart Patterns")
        submitted = st.form_submit_button("➕ Add Category", width="stretch")
        
        if submitted:
            if new_category:
                success, msg = manager.add_category(new_category)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("Category name cannot be empty")


# ============================================================================
# SUBSCRIBER INTERFACE
# ============================================================================

def _subscriber_blog_interface() -> None:
    """Subscriber read-only blog interface"""
    
    st.subheader("📚 Blog & Market Updates")
    
    manager = get_blog_manager()
    published_posts = manager.get_published_posts()
    
    if not published_posts:
        st.info("📭 No blog posts yet. Check back soon!")
        return
    
    st.success(f"✅ {len(published_posts)} articles available")
    
    st.divider()
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_frequency = st.selectbox(
            "Filter by frequency",
            options=["All"] + ["daily", "weekly", "monthly"],
            format_func=lambda x: "All Frequencies" if x == "All" else x.title()
        )
    
    with col2:
        selected_category = st.selectbox(
            "Filter by category",
            options=["All"] + manager.get_categories(),
            format_func=lambda x: "All Categories" if x == "All" else x
        )
    
    with col3:
        sort_order = st.selectbox(
            "Sort by",
            options=["Newest First", "Oldest First"]
        )
    
    # Filter posts
    filtered_posts = published_posts.copy()
    
    if selected_frequency != "All":
        filtered_posts = [p for p in filtered_posts if p['frequency'] == selected_frequency]
    
    if selected_category != "All":
        filtered_posts = [p for p in filtered_posts if p['category'] == selected_category]
    
    if sort_order == "Oldest First":
        filtered_posts = filtered_posts[::-1]
    
    st.divider()
    
    # Display posts
    if not filtered_posts:
        st.warning("No posts match your filters. Try different selections.")
        return
    
    # Show article count
    st.caption(f"📖 Showing {len(filtered_posts)} article(s)")
    
    st.divider()
    
    for post in filtered_posts:
        with st.container(border=True):
            # Header
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"### {post['title']}")
            with col2:
                st.caption(f"🏷️ {post['category']}")
            with col3:
                freq_emoji = "📅" if post['frequency'] == "daily" else "📆" if post['frequency'] == "weekly" else "📊"
                st.caption(f"{freq_emoji} {post['frequency'].title()}")
            
            # Metadata
            st.caption(f"**By:** {post['author']} | **Published:** {post['created_at']}")
            
            st.divider()
            
            # Content
            st.markdown(post['content'])
            
            # Footer
            st.caption(f"👁️ {post.get('views', 0)} views")
    
    st.divider()
    st.caption("💡 New articles are published regularly. Check back for updates!")


if __name__ == "__main__":
    # For standalone testing
    st.set_page_config(page_title="Blog", layout="wide")
    blogpage()
