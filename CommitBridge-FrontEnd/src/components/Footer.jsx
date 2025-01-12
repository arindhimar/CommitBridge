import { Github, Twitter, Linkedin, Instagram, Mail, Globe, Coffee, Heart } from 'lucide-react'
import { motion } from 'framer-motion'

const SocialIcon = ({ href, icon: Icon, label, hoverEffect }) => {
  return (
    <motion.a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={label}
      className="text-foreground hover:text-primary transition-colors"
      whileHover={hoverEffect}
      whileTap={{ scale: 0.9 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
    >
      <Icon className="h-5 w-5" />
    </motion.a>
  )
}

const IconWrapper = ({ children }) => {
  return (
    <motion.div
      className="flex items-center justify-center space-x-8"
      initial="rest"
      animate="rest"
    >
      {children}
    </motion.div>
  )
}

export function Footer() {
  return (
    <footer className="bg-background border-t">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-sm text-muted-foreground">
          <p className="flex items-center justify-center gap-2 mb-4">
            Made with <Heart className="h-4 w-4 text-red-500" /> and <Coffee className="h-4 w-4 text-amber-700" /> by the CommitBridge team
          </p>
          <motion.p
            className="mb-6"
            animate={{ rotate: [-2, 2, -2] }}
            transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
          >
            © {new Date().getFullYear()} CommitBridge. Open source and proud! 🎉
          </motion.p>
        </div>
        <IconWrapper>
          <SocialIcon
            href="https://github.com/arindhimar/commitbridge"
            icon={Github}
            label="GitHub"
            hoverEffect={{ scale: 1.2, rotate: 10 }}
          />
          <SocialIcon
            href="https://twitter.com/arin_dhimar"
            icon={Twitter}
            label="Twitter"
            hoverEffect={{ y: -10, scale: 1.2 }}
          />
          <SocialIcon
            href="https://www.instagram.com/arin_dhimar_"
            icon={Instagram}
            label="Instagram"
            hoverEffect={{ scale: 1.3, rotate: -15 }}
          />
          <SocialIcon
            href="mailto:arindhimar111.com"
            icon={Mail}
            label="Email"
            hoverEffect={{ x: -10, scale: 1.1 }}
          />
          <SocialIcon
            href="https://linkedin.com/company/commitbridge"
            icon={Linkedin}
            label="LinkedIn"
            hoverEffect={{ x: 10, scale: 1.1 }}
          />
          <SocialIcon
            href="https://commitbridge.com"
            icon={Globe}
            label="Portfolio"
            hoverEffect={{ rotate: 360, scale: 1.2 }}
          />
        </IconWrapper>
      </div>
    </footer>
  )
}
