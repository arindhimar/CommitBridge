import { useState, useEffect } from 'react'
import { motion, AnimatePresence, useAnimation } from "framer-motion"
import { Github, Twitter, Linkedin, Clock, Bot, Shield, Moon, Sun, Code, GitBranch, GitCommit, Instagram, ChevronDown, ArrowRight } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useTheme } from "@/components/theme-provider"
import { Link } from 'react-router-dom'
import LoginModal from '@/components/LoginModal'
import { Footer  } from '@/components/Footer'

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6 }
};

export default function LandingPage() {
  const { theme, setTheme } = useTheme()
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false)
  const [expandedFaq, setExpandedFaq] = useState(null)
  const controls = useAnimation()

  useEffect(() => {
    controls.start({
      y: [0, -10, 0],
      transition: { repeat: Infinity, duration: 2 }
    })
  }, [controls])

  const fadeInUp = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  }

  const staggerChildren = {
    animate: {
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const faqData = [
    {
      question: "What is CommitBridge?",
      answer: "CommitBridge is an innovative tool that automates the process of sharing your GitHub activity on social media platforms. It fetches your daily GitHub activity, uses AI to generate concise summaries, and posts them to your chosen social media accounts."
    },
    {
      question: "How does CommitBridge work?",
      answer: "CommitBridge connects to your GitHub account to fetch your activity data. It then uses advanced AI algorithms to analyze this data and create engaging summaries. Finally, it automatically posts these summaries to your linked social media accounts at scheduled intervals."
    },
    {
      question: "Is my GitHub data secure?",
      answer: "Yes, your data security is our top priority. CommitBridge uses secure API connections and doesn't store your GitHub credentials. We only access the public data from your GitHub account that you explicitly allow us to use."
    },
    {
      question: "Which social media platforms are supported?",
      answer: "Currently, CommitBridge supports automatic posting to Twitter and LinkedIn. We're constantly working on expanding our platform support to include more social media networks in the future."
    },
    {
      question: "Can I customize the content of my posts?",
      answer: "While CommitBridge generates summaries automatically, you have full control over the content before it's posted. You can set up custom templates, add specific hashtags, or edit the generated summaries to match your personal style."
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-black text-gray-900 dark:text-white overflow-hidden">
      <nav className="container mx-auto px-4 py-6 flex justify-between items-center">
        <Link to="/" className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-500 to-blue-500">CommitBridge</Link>
        <div className="flex items-center space-x-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            aria-label="Toggle theme"
            className="rounded-full hover:bg-gray-200 dark:hover:bg-gray-800"
          >
            <Sun className="h-6 w-6 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-6 w-6 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          </Button>
        </div>
      </nav>

      <motion.header 
        className="container mx-auto px-4 py-16 text-center relative"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <motion.h1 
          className="text-6xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-teal-500 to-blue-500"
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        >
          CommitBridge: GitHub to Social
        </motion.h1>
        <motion.p 
          className="text-xl text-gray-700 dark:text-gray-300 mb-8"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        >
          Automate Your Daily Work Updates with AI
        </motion.p>
        <Button 
          size="lg" 
          className="bg-gradient-to-r from-teal-500 to-blue-500 hover:from-teal-600 hover:to-blue-600 text-white transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl rounded-full px-8 py-3 text-lg font-semibold"
          onClick={() => setIsLoginModalOpen(true)}
        >
          Get Started Now
          <ArrowRight className="ml-2 h-5 w-5" />
        </Button>
        <motion.div 
          className="absolute bottom-0 left-1/2 transform -translate-x-1/2"
          animate={controls}
        >
          <ChevronDown className="h-8 w-8 text-teal-500" />
        </motion.div>
      </motion.header>

      <main className="container mx-auto px-4 py-12">
        <motion.section 
          className="mb-20"
          variants={staggerChildren}
          initial="initial"
          animate="animate"
        >
          <motion.h2 
            className="text-4xl font-semibold mb-12 text-center bg-clip-text text-transparent bg-gradient-to-r from-teal-500 to-blue-500"
            variants={fadeInUp}
          >
            Key Features
          </motion.h2>
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<Github className="w-12 h-12" />}
              title="Fetch GitHub Activity"
              description="Automatically retrieves your daily GitHub activity, including commits, pull requests, and issues."
            />
            <FeatureCard
              icon={<Bot className="w-12 h-12" />}
              title="AI-Generated Summaries"
              description="Uses AI to create concise, engaging summaries of your technical activities."
            />
            <FeatureCard
              icon={<Twitter className="w-12 h-12" />}
              title="Social Media Integration"
              description="Automatically posts your daily summary to Twitter, LinkedIn, or both."
            />
            <FeatureCard
              icon={<Clock className="w-12 h-12" />}
              title="Daily Automation"
              description="Runs automatically at a set time every day, ensuring consistent posting."
            />
            <FeatureCard
              icon={<Shield className="w-12 h-12" />}
              title="Secure and Scalable"
              description="Securely stores API tokens and can scale to support multiple platforms or users."
            />
            <FeatureCard
              icon={<Linkedin className="w-12 h-12" />}
              title="Multi-Platform Support"
              description="Optionally post the same update across multiple social media platforms simultaneously."
            />
          </div>
        </motion.section>

        <motion.section 
          className="mb-20"
          variants={staggerChildren}
          initial="initial"
          animate="animate"
        >
          <motion.h2 
            className="text-4xl font-semibold mb-12 text-center bg-clip-text text-transparent bg-gradient-to-r from-teal-500 to-blue-500"
            variants={fadeInUp}
          >
            How It Works
          </motion.h2>
          <div className="flex flex-col md:flex-row justify-center items-center space-y-8 md:space-y-0 md:space-x-8">
            <WorkflowCard
              icon={<GitCommit className="w-8 h-8" />}
              title="Commit"
              description="You push your code changes to GitHub as usual."
            />
            <GitBranch className="w-8 h-8 text-teal-500 transform rotate-90 md:rotate-0" />
            <WorkflowCard
              icon={<Bot className="w-8 h-8" />}
              title="Process"
              description="CommitBridge fetches your activity and generates a summary using AI."
            />
            <GitBranch className="w-8 h-8 text-teal-500 transform rotate-90 md:rotate-0" />
            <WorkflowCard
              icon={<Code className="w-8 h-8" />}
              title="Share"
              description="Your activity summary is automatically posted to your chosen social platforms."
            />
          </div>
        </motion.section>

        <motion.section 
          className="mb-20"
          variants={staggerChildren}
          initial="initial"
          animate="animate"
        >
          <motion.h2 
            className="text-4xl font-semibold mb-12 text-center bg-clip-text text-transparent bg-gradient-to-r from-teal-500 to-blue-500"
            variants={fadeInUp}
          >
            Frequently Asked Questions
          </motion.h2>
          <div className="w-full max-w-3xl mx-auto">
            {faqData.map((faq, index) => (
              <motion.div
                key={index}
                className="mb-4"
                initial={false}
                animate={{ backgroundColor: expandedFaq === index ? 'rgba(20, 184, 166, 0.1)' : 'transparent' }}
                transition={{ duration: 0.3 }}
              >
                <motion.button
                  className="flex justify-between items-center w-full px-6 py-4 text-lg font-medium text-left text-gray-800 dark:text-gray-200 focus:outline-none focus-visible:ring focus-visible:ring-teal-500 focus-visible:ring-opacity-75 rounded-lg hover:bg-gradient-to-r hover:from-teal-50 hover:to-blue-50 dark:hover:from-teal-900/20 dark:hover:to-blue-900/20 transition-all duration-300"
                  onClick={() => setExpandedFaq(expandedFaq === index ? null : index)}
                >
                  <span>{faq.question}</span>
                  <ChevronDown
                    className={`w-6 h-6 text-teal-500 transition-transform duration-300 ${
                      expandedFaq === index ? 'transform rotate-180' : ''
                    }`}
                  />
                </motion.button>
                <AnimatePresence initial={false}>
                  {expandedFaq === index && (
                    <motion.div
                      initial="collapsed"
                      animate="expanded"
                      exit="collapsed"
                      variants={{
                        expanded: { opacity: 1, height: 'auto', marginTop: 8 },
                        collapsed: { opacity: 0, height: 0, marginTop: 0 }
                      }}
                      transition={{ duration: 0.4, ease: [0.04, 0.62, 0.23, 0.98] }}
                    >
                      <motion.div
                        variants={{ collapsed: { scale: 0.8 }, expanded: { scale: 1 } }}
                        transition={{ duration: 0.4 }}
                        className="text-gray-600 dark:text-gray-300 px-6 pb-4 bg-gradient-to-r from-teal-50 to-blue-50 dark:from-teal-900/10 dark:to-blue-900/10 rounded-b-lg"
                      >
                        {faq.answer}
                      </motion.div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            ))}
          </div>
        </motion.section>
      </main>

      <Footer />

      {/* <footer className="bg-gray-100 dark:bg-gray-900 text-center py-8 mt-16">
        <div className="container mx-auto px-4">
          <p className="mb-4 text-gray-700 dark:text-gray-300">&copy; 2023 CommitBridge. All rights reserved.</p>
          <div className="flex justify-center space-x-6">
            <SocialLink href="https://x.com/arin_dhimar" icon={<Twitter className="w-6 h-6" />} />
            <SocialLink href="https://github.com/arindhimar" icon={<Github className="w-6 h-6" />} />
            <SocialLink href="https://www.linkedin.com/in/arin-dhimar" icon={<Linkedin className="w-6 h-6" />} />
            <SocialLink href="https://www.instagram.com/arin_dhimar_" icon={<Instagram className="w-6 h-6" />} />
          </div>
        </div>
      </footer> */}

      <LoginModal isOpen={isLoginModalOpen} onClose={() => setIsLoginModalOpen(false)} />
    </div>
  )
}

function FeatureCard({ icon, title, description }) {
  return (
    <motion.div initial="initial" animate="animate" variants={fadeInUp}>
      <Card className="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-300 transform hover:scale-105 hover:shadow-xl rounded-lg overflow-hidden">
        <CardHeader>
          <CardTitle className="flex flex-col items-center gap-4 text-teal-600 dark:text-teal-400">
            <motion.div
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.5 }}
            >
              {icon}
            </motion.div>
            <span className="text-xl">{title}</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <CardDescription className="text-gray-600 dark:text-gray-300 text-center">{description}</CardDescription>
        </CardContent>
      </Card>
    </motion.div>
  )
}

function WorkflowCard({ icon, title, description }) {
  return (
    <motion.div initial="initial" animate="animate" variants={fadeInUp}>
      <Card className="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-300 transform hover:scale-105 hover:shadow-xl rounded-lg overflow-hidden w-full md:w-64">
      <CardHeader>
        <CardTitle className="flex flex-col items-center gap-4 text-teal-600 dark:text-teal-400">
          <motion.div
            whileHover={{ rotate: 360 }}
            transition={{ duration: 0.5 }}
          >
            {icon}
          </motion.div>
          <span className="text-xl">{title}</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <CardDescription className="text-gray-600 dark:text-gray-300 text-center">{description}</CardDescription>
      </CardContent>
    </Card>
  </motion.div>
  )
}

function SocialLink({ href, icon }) {
  return (
    <motion.a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="text-gray-600 hover:text-teal-500 dark:text-gray-400 dark:hover:text-teal-300 transition-colors"
      whileHover={{ scale: 1.2 }}
      whileTap={{ scale: 0.9 }}
    >
      {icon}
    </motion.a>
  )
}

