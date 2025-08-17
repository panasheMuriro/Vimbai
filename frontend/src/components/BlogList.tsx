// src/components/BlogList.tsx
import { useEffect, useState } from "react";
import { collection, getDocs } from "firebase/firestore";
import { db } from "../../utils/firebase";
import BlogCard from "./BlogCard";

interface Blog {
  category: string;
  content: string;
}

interface BlogGroup {
  date: string;
  blogs: Blog[];
}

export default function BlogList() {
  const [groupedBlogs, setGroupedBlogs] = useState<BlogGroup[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        const snapshot = await getDocs(collection(db, "blogs_test"));
        if (snapshot.empty) {
          setGroupedBlogs([]);
          return;
        }

        const grouped: BlogGroup[] = snapshot.docs.map((doc) => {
          const docData = doc.data();
          const date = doc.id; // assuming doc.id is the date string
          const blogs: Blog[] = Object.keys(docData)
            .filter((key) => key !== "id")
            .map((category) => ({
              category,
              content: docData[category],
            }));

          return { date, blogs };
        });

        // Sort newest first
        grouped.sort((a, b) => (a.date < b.date ? 1 : -1));

        setGroupedBlogs(grouped);
      } catch (error) {
        console.error("Error fetching blogs:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchBlogs();
  }, []);

  if (loading) return  <div className="flex justify-center items-center h-40">
      <div className="w-18 h-18 border-4 border-[#e76f51] border-t-transparent rounded-full animate-spin"></div>
    </div>


  return (
    <div className="p-4 max-w-2xl mx-auto space-y-6">
      {groupedBlogs.map((group) => (
        <div key={group.date}>
          <h2 className="text-xl font-bold mb-3 text-center text-gray-500">{group.date}</h2>
          <div className="space-y-4">
            {group.blogs.map((post, index) => (
              <BlogCard
                key={index}
                category={post.category}
                content={post.content}
                date={group.date}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
