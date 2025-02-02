import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export default function ProfilePage() {
  return (
    <div className="min-h-screen bg-black text-white">
      {/* Profile Content */}
      <div className="container mx-auto px-4 pt-8">
        <div className="flex flex-col gap-8 max-w-3xl">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-h1 font-bold text-white">Profile Settings</h1>
              <p className="text-muted-foreground">
                Manage your account settings and preferences
              </p>
            </div>
            <Button variant="outline" className="bg-white text-black border-white hover:bg-white/90">
              View Public Profile
            </Button>
          </div>

          <Card className="p-6 bg-black border-white/20">
            <form className="space-y-8">
              <div className="space-y-6">
                <div>
                  <h2 className="text-h3 font-semibold mb-4 text-white">Personal Info</h2>
                  <p className="text-sm text-muted-foreground mb-4">
                    Update your personal information and how others see you on the platform.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-white">Full Name</label>
                    <Input placeholder="Enter your full name" className="bg-black border-white/20 text-white" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-white">Email Address</label>
                    <Input type="email" placeholder="you@example.com" className="bg-black border-white/20 text-white" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-white">Account Type</label>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="outline" className="w-full justify-start text-left font-normal bg-white text-black border-white hover:bg-white/90">
                          Select Account Type
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent className="bg-black border-white/20">
                        <DropdownMenuItem className="text-white hover:bg-white/10">
                          Paper Trading
                        </DropdownMenuItem>
                        <DropdownMenuItem className="text-white hover:bg-white/10">
                          Live Trading
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-white">Profile Picture</label>
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 rounded-full border-2 border-dashed border-white/20 flex items-center justify-center">
                      <img
                        src="/placeholder-avatar.png"
                        alt="Avatar"
                        className="w-full h-full rounded-full object-cover"
                      />
                    </div>
                    <div className="flex-1">
                      <Button variant="outline" className="mr-2 bg-white text-black border-white hover:bg-white/90">
                        Change Avatar
                      </Button>
                      <Button variant="ghost" className="text-destructive hover:text-destructive/90">
                        Remove
                      </Button>
                      <p className="text-xs text-muted-foreground mt-2">
                        Supported formats: SVG, PNG, JPG (10mb max)
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-end gap-4">
                <Button variant="outline" className="bg-white text-black border-white hover:bg-white/90">
                  Cancel
                </Button>
                <Button className="bg-yellow-500 text-black hover:bg-yellow-400">
                  Save Changes
                </Button>
              </div>
            </form>
          </Card>
        </div>
      </div>
    </div>
  )
} 