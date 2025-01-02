import { Link } from 'react-router-dom'
import { Github, Twitter, Linkedin, Coffee, Heart } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function Footer() {
  return (
    <footer className="bg-background border-t">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="space-y-4">
            <Link to="/" className="text-2xl font-bold text-primary">
              CommitBridge
            </Link>
            <p className="text-sm text-muted-foreground">
              Turning your commits into cool social posts! 🚀
            </p>
            <div className="flex space-x-4">
              <a href="https://github.com/commitbridge" target="_blank" rel="noopener noreferrer" className="text-foreground hover:text-primary transition-colors">
                <Github className="h-5 w-5" />
              </a>
              <a href="https://twitter.com/commitbridge" target="_blank" rel="noopener noreferrer" className="text-foreground hover:text-primary transition-colors">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="https://linkedin.com/company/commitbridge" target="_blank" rel="noopener noreferrer" className="text-foreground hover:text-primary transition-colors">
                <Linkedin className="h-5 w-5" />
              </a>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4 text-foreground">Quick Links</h3>
            <nav className="space-y-2">
              <Link to="/about" className="block text-muted-foreground hover:text-primary transition-colors">About This Project</Link>
              <Link to="/features" className="block text-muted-foreground hover:text-primary transition-colors">Cool Features</Link>
              <Link to="/contribute" className="block text-muted-foreground hover:text-primary transition-colors">Contribute</Link>
              <Link to="/showcase" className="block text-muted-foreground hover:text-primary transition-colors">User Showcase</Link>
            </nav>
          </div>
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-foreground">Stay in the Loop!</h3>
            <p className="text-sm text-muted-foreground">Get notified about new features and updates.</p>
            <form className="flex space-x-2">
              <Input 
                type="email" 
                placeholder="Your email" 
                className="bg-background text-foreground border-primary"
              />
              <Button type="submit" variant="outline">Join</Button>
            </form>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-muted text-center text-sm text-muted-foreground">
          <p className="flex items-center justify-center gap-2">
            Made with <Heart className="h-4 w-4 text-red-500" /> and <Coffee className="h-4 w-4 text-amber-700" /> by the CommitBridge team
          </p>
          <p className="mt-2">
            © {new Date().getFullYear()} CommitBridge. Open source and proud! 🎉
          </p>
        </div>
      </div>
    </footer>
  )
}

