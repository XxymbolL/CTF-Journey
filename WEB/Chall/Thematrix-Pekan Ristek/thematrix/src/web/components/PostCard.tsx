import { Post } from "@/lib/types";
import { FaHeart } from "react-icons/fa";

export interface PostCardProps {
    post: Post;
}

const PostCard: React.FC<PostCardProps> = ({ post }) => {
    return (
        <div className="flex flex-col gap-4 p-4 bg-stone-800 rounded-lg">
            <a href={`/${post.author}`} className="flex items-center gap-2 hover:underline hover:underline-offset-4 text-xl font-bold">
                @{post.author}
            </a>
            <div>
                <p>{post.content}</p>
                <div className="flex gap-2 items-center justify-end">
                    <FaHeart className="text-red-500" />
                    <p>{post.likes}</p>
                </div>
            </div>
        </div>
    );
}

export default PostCard;
