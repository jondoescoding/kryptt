import Link from "next/link"
import { ThemeToggle } from "../ui/theme-toggle"

export function Footer() {
  return (
    <footer className="border-t font-[family-name:var(--font-roc-grotesk)]">
      <div className="container flex flex-col gap-8 py-8 px-4 md:py-12">
        <div className="flex flex-col md:flex-row justify-between gap-8">
          <div className="space-y-4">
            <h3 className="text-xl font-bold tracking-tight">nightshade-ai</h3>
            <p className="text-sm text-muted-foreground max-w-xs">
              Building the future of AI, one line at a time.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h4 className="font-medium tracking-tight">Quick Links</h4>
            <nav className="flex flex-col space-y-2">
              <Link href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Home
              </Link>
              <Link href="/about" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                About
              </Link>
              <Link href="/chat" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Chat
              </Link>
              <Link href="/dashboard" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Dashboard
              </Link>
              <Link href="/contact" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Contact
              </Link>
            </nav>
          </div>

          {/* Social & Contact */}
          <div className="space-y-4">
            <h4 className="font-medium tracking-tight">Follow Us</h4>
            <div className="flex items-center space-x-2">
              <Link 
                href="https://twitter.com/jondoescoding" 
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                @jondoescoding
              </Link>
            </div>
            
            <div className="space-y-2 mt-4">
              <h4 className="font-medium tracking-tight">Location</h4>
              <p className="text-sm text-muted-foreground">Bowtied Island</p>
            </div>
          </div>

          {/* Theme Toggle */}
          <div className="space-y-4">
            <h4 className="font-medium tracking-tight">Theme</h4>
            <ThemeToggle />
          </div>
        </div>
      </div>
      
      <div className="border-t w-full">
        <div className="max-w-screen-2xl mx-auto px-4">
          <p className="text-sm text-muted-foreground text-center py-8">
            © {new Date().getFullYear()} nightshade-ai. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
} 