'use client';

import { useState, useEffect } from "react";
import { User, Post } from "@/lib/types";
import PostCard from "@/components/PostCard";

export interface UserPageProps {
  params: {
    username: string;
  };
}

export default function UserPage({ params }: UserPageProps) {
  const [user, setUser] = useState<User>();
  const [userPosts, setUserPosts] = useState<Post[]>([]);
  const [isPrivate, setIsPrivate] = useState(false);
  const [followers, setFollowers] = useState<number>(0);
  const [following, setFollowing] = useState<number>(0);
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/users?username=${params.username}`)
      .then((res) => res.json())
      .then((data) => setUser(data.data))
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/posts?username=${params.username}`)
      .then((res) => {
        if (res.status === 401) {
          setIsPrivate(true);
        }
        return res.json();
      })
      .then((data) => setUserPosts(data.data))
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/users/followers?username=${params.username}`)
      .then((res) => res.json())
      .then((data) => setFollowers(data.data.length))
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/users/following?username=${params.username}`)
      .then((res) => res.json())
      .then((data) => setFollowing(data.data.length))
  }, [params.username]);
  return (
    <div className="flex flex-col items-center min-h-screen p-16 gap-8">
      <a href="/" className="text-5xl font-black">thematrix</a>
      <div className="flex flex-col gap-4 w-1/2 p-8 bg-stone-700 rounded-xl">
        <h1 className="text-2xl font-bold">@{user?.username}</h1>
        <p>{user?.description}</p>
        <div className="flex gap-4">
          <p>{followers} Followers</p>
          <p>{following} Following</p>
        </div>
        {isPrivate ? (
          <div className="flex flex-col justify-center items-center text-xl">
            <p>This user is private</p>
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            {userPosts.map((post, index) => (
              <div key={index}>
                <PostCard post={post} />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
