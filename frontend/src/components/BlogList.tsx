// src/components/BlogList.tsx
import { useEffect, useState } from "react";
import { collection, getDocs } from "firebase/firestore";
import { db } from "../../utils/firebase";
import BlogCard from "./BlogCard";

interface Blog {
  id: string;
  category: string;
  content: string;
  date: string;
}

export default function BlogList() {
  const [blogs, setBlogs] = useState<Blog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        const snapshot = await getDocs(collection(db, "blogs_test"));
        const docData = snapshot.docs[0]?.data();
        if (!docData) return;

        const docId = snapshot.docs[0].id;

        const formattedBlogs: Blog[] = Object.keys(docData)
          .filter((key) => key !== "id")
          .map((category) => ({
            id: docId,
            category,
            content: docData[category],
            date: docData["id"] || new Date().toISOString().split("T")[0],
          }));

        setBlogs(formattedBlogs);
      } catch (error) {
        console.error("Error fetching blogs:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchBlogs();
  }, []);

  if (loading) return <p>Loading blogs...</p>;

  return (
    <div className="p-4 max-w-md mx-auto">
      {blogs.map((post, index) => (
        <BlogCard
          key={index}
          category={post.category}
          content={post.content}
          date={post.date}
        />
      ))}
    </div>
  );
}
