"""
🚀 BLOG MANAGER - Backend Logic for Blog System
===============================================

Handles all blog operations:
- Create, read, update, delete blog posts
- Frequency management (daily/weekly/monthly)
- Category management
- Published/Draft status
- Author tracking
- Timestamp management

Production-ready with error handling and validation.
"""

import json
import os
from datetime import datetime
import pytz
from typing import List, Dict, Optional, Tuple


class BlogManager:
    """
    Complete blog management system with CRUD operations,
    frequency settings, and role-based access control.
    
    Database: JSON file (blog_database.json)
    """
    
    def __init__(self, db_path: str = "blog_database.json"):
        """
        Initialize BlogManager with database path.
        Auto-creates database if it doesn't exist.
        
        Args:
            db_path: Path to blog_database.json
        """
        self.db_path = db_path
        self.tz = pytz.timezone("Asia/Kolkata")
        self._ensure_database()
    
    def _ensure_database(self) -> None:
        """Create database file if it doesn't exist"""
        if not os.path.exists(self.db_path):
            self._init_database()
    
    def _init_database(self) -> None:
        """Initialize empty blog database"""
        initial_db = {
            "posts": [],
            "categories": ["Sector News", "ETF Updates", "Market Insights", "Trading Tips", "Analysis"],
            "created_at": self._get_timestamp(),
            "version": "1.0"
        }
        self._save_database(initial_db)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in IST"""
        return datetime.now(self.tz).strftime("%Y-%m-%d %H:%M:%S IST")
    
    def _load_database(self) -> Dict:
        """Load entire database from JSON"""
        try:
            if not os.path.exists(self.db_path):
                self._init_database()
            
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error loading database: {str(e)}")
    
    def _save_database(self, data: Dict) -> None:
        """Save entire database to JSON"""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Error saving database: {str(e)}")
    
    # ========================================================================
    # POST OPERATIONS (CRUD)
    # ========================================================================
    
    def create_post(
        self,
        title: str,
        content: str,
        author: str,
        frequency: str = "weekly",
        category: str = "Sector News",
        status: str = "draft"
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Create a new blog post.
        
        Args:
            title: Post title
            content: Post content (markdown supported)
            author: Author username
            frequency: daily/weekly/monthly
            category: Blog category
            status: draft/published
        
        Returns:
            (success, message, post_id)
        """
        try:
            if not title or len(title.strip()) == 0:
                return False, "Title cannot be empty", None
            
            if not content or len(content.strip()) == 0:
                return False, "Content cannot be empty", None
            
            if frequency not in ["daily", "weekly", "monthly"]:
                return False, "Invalid frequency. Use: daily, weekly, monthly", None
            
            db = self._load_database()
            
            # Generate post ID
            post_id = f"post_{len(db['posts']) + 1}_{int(datetime.now(self.tz).timestamp())}"
            
            # Create post object
            post = {
                "id": post_id,
                "title": title.strip(),
                "content": content.strip(),
                "author": author,
                "frequency": frequency,
                "category": category,
                "status": status,
                "created_at": self._get_timestamp(),
                "updated_at": self._get_timestamp(),
                "views": 0
            }
            
            db['posts'].append(post)
            self._save_database(db)
            
            return True, f"✅ Post '{title}' created successfully!", post_id
        
        except Exception as e:
            return False, f"Error creating post: {str(e)}", None
    
    def get_all_posts(self, status: Optional[str] = None) -> List[Dict]:
        """
        Get all posts (optionally filtered by status).
        
        Args:
            status: 'published', 'draft', or None for all
        
        Returns:
            List of post dictionaries
        """
        try:
            db = self._load_database()
            posts = db.get('posts', [])
            
            if status:
                posts = [p for p in posts if p.get('status') == status]
            
            # Sort by created_at descending (newest first)
            return sorted(posts, key=lambda x: x.get('created_at', ''), reverse=True)
        
        except Exception as e:
            raise Exception(f"Error getting posts: {str(e)}")
    
    def get_published_posts(self) -> List[Dict]:
        """Get only published posts"""
        return self.get_all_posts(status='published')
    
    def get_posts_by_frequency(self, frequency: str) -> List[Dict]:
        """Get published posts by frequency"""
        try:
            posts = self.get_published_posts()
            return [p for p in posts if p.get('frequency') == frequency]
        except Exception as e:
            raise Exception(f"Error filtering by frequency: {str(e)}")
    
    def get_posts_by_category(self, category: str) -> List[Dict]:
        """Get published posts by category"""
        try:
            posts = self.get_published_posts()
            return [p for p in posts if p.get('category') == category]
        except Exception as e:
            raise Exception(f"Error filtering by category: {str(e)}")
    
    def get_post_by_id(self, post_id: str) -> Optional[Dict]:
        """Get a specific post by ID"""
        try:
            posts = self.get_all_posts()
            for post in posts:
                if post.get('id') == post_id:
                    return post
            return None
        except Exception as e:
            raise Exception(f"Error getting post: {str(e)}")
    
    def update_post(
        self,
        post_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        frequency: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Update an existing blog post.
        
        Args:
            post_id: Post ID to update
            title: New title (optional)
            content: New content (optional)
            frequency: New frequency (optional)
            category: New category (optional)
            status: New status (optional)
        
        Returns:
            (success, message)
        """
        try:
            db = self._load_database()
            post = None
            post_index = -1
            
            for i, p in enumerate(db['posts']):
                if p.get('id') == post_id:
                    post = p
                    post_index = i
                    break
            
            if post is None:
                return False, "Post not found"
            
            # Update fields
            if title:
                post['title'] = title.strip()
            if content:
                post['content'] = content.strip()
            if frequency and frequency in ["daily", "weekly", "monthly"]:
                post['frequency'] = frequency
            if category:
                post['category'] = category
            if status and status in ["draft", "published"]:
                post['status'] = status
            
            post['updated_at'] = self._get_timestamp()
            
            db['posts'][post_index] = post
            self._save_database(db)
            
            return True, f"✅ Post updated successfully!"
        
        except Exception as e:
            return False, f"Error updating post: {str(e)}"
    
    def delete_post(self, post_id: str) -> Tuple[bool, str]:
        """
        Delete a blog post.
        
        Args:
            post_id: Post ID to delete
        
        Returns:
            (success, message)
        """
        try:
            db = self._load_database()
            original_count = len(db['posts'])
            
            db['posts'] = [p for p in db['posts'] if p.get('id') != post_id]
            
            if len(db['posts']) == original_count:
                return False, "Post not found"
            
            self._save_database(db)
            return True, "✅ Post deleted successfully!"
        
        except Exception as e:
            return False, f"Error deleting post: {str(e)}"
    
    # ========================================================================
    # CATEGORY OPERATIONS
    # ========================================================================
    
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        try:
            db = self._load_database()
            return db.get('categories', [])
        except Exception as e:
            raise Exception(f"Error getting categories: {str(e)}")
    
    def add_category(self, category: str) -> Tuple[bool, str]:
        """Add a new category"""
        try:
            db = self._load_database()
            categories = db.get('categories', [])
            
            if category in categories:
                return False, "Category already exists"
            
            categories.append(category)
            db['categories'] = categories
            self._save_database(db)
            
            return True, f"✅ Category '{category}' added!"
        
        except Exception as e:
            return False, f"Error adding category: {str(e)}"
    
    def delete_category(self, category: str) -> Tuple[bool, str]:
        """Delete a category"""
        try:
            db = self._load_database()
            categories = db.get('categories', [])
            
            if category not in categories:
                return False, "Category not found"
            
            categories.remove(category)
            db['categories'] = categories
            self._save_database(db)
            
            return True, f"✅ Category '{category}' deleted!"
        
        except Exception as e:
            return False, f"Error deleting category: {str(e)}"
    
    # ========================================================================
    # STATISTICS
    # ========================================================================
    
    def get_statistics(self) -> Dict:
        """Get blog statistics"""
        try:
            db = self._load_database()
            posts = db.get('posts', [])
            
            return {
                "total_posts": len(posts),
                "published": sum(1 for p in posts if p.get('status') == 'published'),
                "drafts": sum(1 for p in posts if p.get('status') == 'draft'),
                "daily": sum(1 for p in posts if p.get('frequency') == 'daily' and p.get('status') == 'published'),
                "weekly": sum(1 for p in posts if p.get('frequency') == 'weekly' and p.get('status') == 'published'),
                "monthly": sum(1 for p in posts if p.get('frequency') == 'monthly' and p.get('status') == 'published'),
                "categories": len(db.get('categories', [])),
                "db_created": db.get('created_at', 'Unknown'),
                "version": db.get('version', '1.0')
            }
        except Exception as e:
            raise Exception(f"Error getting statistics: {str(e)}")


# ============================================================================
# STANDALONE HELPER FUNCTIONS
# ============================================================================

def get_blog_manager() -> BlogManager:
    """Get or create a BlogManager instance"""
    return BlogManager("blog_database.json")


def preview_subscriber_view(limit: int = 5) -> List[Dict]:
    """
    Preview what subscribers will see.
    Returns latest published posts with all details.
    """
    manager = get_blog_manager()
    posts = manager.get_published_posts()
    return posts[:limit]


def get_dashboard_stats() -> Dict:
    """Get blog dashboard statistics"""
    manager = get_blog_manager()
    return manager.get_statistics()
