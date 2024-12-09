'use client';

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Post } from "@/lib/types";
import PostCard from "@/components/PostCard";

export default function Home() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [userSearch, setUserSearch] = useState<string>("");
  const router = useRouter();
  const handler = (e: React.KeyboardEvent<HTMLInputElement>) => {
    setUserSearch(e.currentTarget.value);
    if (e.key === "Enter") {
      router.push(`/${userSearch}`);
      return
    }
  };
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/posts`)
      .then((res) => res.json())
      .then((data) => setPosts(data.data))
  }, []);
  return (
    <div className="flex flex-col items-center min-h-screen p-16 gap-8">
      <a href="/" className="text-5xl font-black">thematrix</a>
      <input type="text" className="bg-stone-700 py-2 px-4 rounded-xl" placeholder="Find user..." onKeyUp={handler} />
      <div className="flex flex-col gap-4 w-1/2">
        {posts.map((post, index) => (
          <div key={index}>
            <PostCard post={post} />
          </div>
        ))}
      </div>
    </div>
  );
}
