import { handleAuth } from "@kinde-oss/kinde-auth-nextjs/server";

// This will handle all auth routes including login, register, and logout
export const GET = handleAuth(); 