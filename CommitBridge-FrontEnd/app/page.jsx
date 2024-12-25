'use client'

import { useState } from 'react'
import { motion } from "framer-motion"
import { Github, Twitter, Linkedin, Clock, Bot, Shield, Moon, Sun, Code, GitBranch, GitCommit } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useTheme } from "next-themes"
import Link from 'next/link'
import LoginModal from '@/components/LoginModal'

export default function LandingPage() {
  const { theme, setTheme } = useTheme()
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false)

  const fadeIn = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-100 to-gray-200 dark:from-gray-900 dark:to-black text-gray-900 dark:text-white">
      <nav className="container mx-auto px-4 py-6 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold">CommitBridge</Link>
        <div className="flex items-center space-x-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            aria-label="Toggle theme"
          >
            <Sun className="h-6 w-6 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-6 w-6 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          </Button>
        </div>
      </nav>

      <motion.header 
        className="container mx-auto px-4 py-16 text-center"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <h1 className="text-5xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-teal-600 to-blue-600 dark:from-teal-400 dark:to-blue-400">
          CommitBridge: GitHub to Social
        </h1>
        <p className="text-xl text-gray-700 dark:text-gray-300 mb-8">Automate Your Daily Work Updates with AI</p>
        <Button 
          size="lg" 
          className="bg-gradient-to-r from-teal-500 to-blue-500 hover:from-teal-600 hover:to-blue-600 text-white transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
          onClick={() => setIsLoginModalOpen(true)}
        >
          Get Started Now
        </Button>
      </motion.header>

      <main className="container mx-auto px-4 py-12">
        <motion.section className="mb-20" {...fadeIn}>
          <h2 className="text-3xl font-semibold mb-12 text-center text-teal-300 dark:text-teal-400">Key Features</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<Github className="w-10 h-10" />}
              title="Fetch GitHub Activity"
              description="Automatically retrieves your daily GitHub activity, including commits, pull requests, and issues."
            />
            <FeatureCard
              icon={<Bot className="w-10 h-10" />}
              title="AI-Generated Summaries"
              description="Uses AI to create concise, engaging summaries of your technical activities."
            />
            <FeatureCard
              icon={<Twitter className="w-10 h-10" />}
              title="Social Media Integration"
              description="Automatically posts your daily summary to Twitter, LinkedIn, or both."
            />
            <FeatureCard
              icon={<Clock className="w-10 h-10" />}
              title="Daily Automation"
              description="Runs automatically at a set time every day, ensuring consistent posting."
            />
            <FeatureCard
              icon={<Shield className="w-10 h-10" />}
              title="Secure and Scalable"
              description="Securely stores API tokens and can scale to support multiple platforms or users."
            />
            <FeatureCard
              icon={<Linkedin className="w-10 h-10" />}
              title="Multi-Platform Support"
              description="Optionally post the same update across multiple social media platforms simultaneously."
            />
          </div>
        </motion.section>

        <motion.section className="mb-20" {...fadeIn}>
          <h2 className="text-3xl font-semibold mb-12 text-center text-teal-300 dark:text-teal-400">How It Works</h2>
          <div className="flex flex-col md:flex-row justify-center items-center space-y-8 md:space-y-0 md:space-x-8">
            <Card className="bg-gray-800 dark:bg-gray-900 border-gray-700 w-full md:w-1/3">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-teal-300 dark:text-teal-400">
                  <GitCommit className="w-6 h-6" />
                  <span>Commit</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-300 dark:text-gray-400">
                  You push your code changes to GitHub as usual.
                </CardDescription>
              </CardContent>
            </Card>
            <GitBranch className="w-8 h-8 text-teal-300 dark:text-teal-400 transform rotate-90 md:rotate-0" />
            <Card className="bg-gray-800 dark:bg-gray-900 border-gray-700 w-full md:w-1/3">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-teal-300 dark:text-teal-400">
                  <Bot className="w-6 h-6" />
                  <span>Process</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-300 dark:text-gray-400">
                  CommitBridge fetches your activity and generates a summary using AI.
                </CardDescription>
              </CardContent>
            </Card>
            <GitBranch className="w-8 h-8 text-teal-300 dark:text-teal-400 transform rotate-90 md:rotate-0" />
            <Card className="bg-gray-800 dark:bg-gray-900 border-gray-700 w-full md:w-1/3">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-teal-300 dark:text-teal-400">
                  <Code className="w-6 h-6" />
                  <span>Share</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-300 dark:text-gray-400">
                  Your activity summary is automatically posted to your chosen social platforms.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </motion.section>

        <motion.section className="text-center mb-20" {...fadeIn}>
          <h2 className="text-3xl font-semibold mb-8 text-teal-300 dark:text-teal-400">Ready to Bridge Your Commits?</h2>
          <Button size="lg" className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl">
            Get Started Now
          </Button>
        </motion.section>
      </main>

      <footer className="bg-gray-200 dark:bg-gray-900 text-center py-6 mt-16">
        <div className="container mx-auto px-4">
          <p className="mb-4 text-gray-700 dark:text-gray-300">&copy; 2023 CommitBridge. All rights reserved.</p>
          <div className="flex justify-center space-x-4">
            <a href="#" className="text-gray-600 hover:text-teal-500 dark:text-gray-400 dark:hover:text-teal-300 transition-colors">
              <Twitter className="w-6 h-6" />
            </a>
            <a href="#" className="text-gray-600 hover:text-teal-500 dark:text-gray-400 dark:hover:text-teal-300 transition-colors">
              <Github className="w-6 h-6" />
            </a>
            <a href="#" className="text-gray-600 hover:text-teal-500 dark:text-gray-400 dark:hover:text-teal-300 transition-colors">
              <Linkedin className="w-6 h-6" />
            </a>
          </div>
        </div>
      </footer>

      <LoginModal isOpen={isLoginModalOpen} onClose={() => setIsLoginModalOpen(false)} />
    </div>
  )
}

function FeatureCard({ icon, title, description }) {
  return (
    <Card className="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-300 transform hover:scale-105 hover:shadow-xl">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-teal-600 dark:text-teal-400">
          {icon}
          <span>{title}</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <CardDescription className="text-gray-600 dark:text-gray-300">{description}</CardDescription>
      </CardContent>
    </Card>
  )
}

