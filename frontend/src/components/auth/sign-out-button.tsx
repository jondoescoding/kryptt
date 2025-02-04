'use client'

import { Button } from '@/components/ui/button'
import { createClient } from '@/lib/supabase/client'
import { LogOut } from 'lucide-react'

export function SignOutButton() {
  const handleSignOut = async () => {
    const supabase = createClient()
    await supabase.auth.signOut()
    window.location.href = '/' // Redirect to landing page after sign out
  }

  return (
    <Button 
      onClick={handleSignOut} 
      variant="ghost" 
      size="sm"
      className="text-white/70 hover:text-yellow-400 hover:bg-transparent"
    >
      <LogOut className="h-4 w-4 mr-2" />
      Sign Out
    </Button>
  )
} 