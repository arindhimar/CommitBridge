import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { GitBranch, Twitter, Linkedin, Clock, BarChart, GitCommit, MessageSquare, Plus, X } from 'lucide-react'
import { Header } from '@/components/Header'
import { Footer } from '@/components/Footer'

export default function Dashboard() {
  const [gitRepos, setGitRepos] = useState([''])
  const [trackInterval, setTrackInterval] = useState('daily')
  const [twitterEnabled, setTwitterEnabled] = useState(false)
  const [linkedinEnabled, setLinkedinEnabled] = useState(false)
  const [user, setUser] = useState(null)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
  }, [])

  const handleAddRepo = () => {
    setGitRepos([...gitRepos, ''])
  }

  const handleRemoveRepo = (index) => {
    const newRepos = gitRepos.filter((_, i) => i !== index)
    setGitRepos(newRepos)
  }

  const handleRepoChange = (index, value) => {
    const newRepos = [...gitRepos]
    newRepos[index] = value
    setGitRepos(newRepos)
  }

  const handleSaveSettings = () => {
    // TODO: Implement saving settings to backend
    console.log('Saving settings:', { gitRepos, trackInterval, twitterEnabled, linkedinEnabled })
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow">
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="container mx-auto p-4 space-y-6"
        >
          <h1 className="text-3xl font-bold">Dashboard</h1>

          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Commits</CardTitle>
                <GitCommit className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">1,234</div>
                <p className="text-xs text-muted-foreground">+20.1% from last month</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Social Shares</CardTitle>
                <MessageSquare className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">423</div>
                <p className="text-xs text-muted-foreground">+15% from last month</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Engagement Rate</CardTitle>
                <BarChart className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">5.2%</div>
                <p className="text-xs text-muted-foreground">+2.1% from last month</p>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="grid grid-cols-1 md:grid-cols-2 gap-6"
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <GitBranch className="w-6 h-6" />
                  Git Integration
                </CardTitle>
                <CardDescription>Configure your Git repository settings</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {gitRepos.map((repo, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <Input
                        placeholder="https://github.com/username/repo.git"
                        value={repo}
                        onChange={(e) => handleRepoChange(index, e.target.value)}
                      />
                      {index > 0 && (
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleRemoveRepo(index)}
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  ))}
                  <Button
                    variant="outline"
                    size="sm"
                    className="mt-2"
                    onClick={handleAddRepo}
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Add Repository
                  </Button>
                  <div>
                    <Label htmlFor="track-interval">Commit Tracking Interval</Label>
                    <Select value={trackInterval} onValueChange={setTrackInterval}>
                      <SelectTrigger id="track-interval">
                        <SelectValue placeholder="Select interval" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="hourly">Hourly</SelectItem>
                        <SelectItem value="daily">Daily</SelectItem>
                        <SelectItem value="weekly">Weekly</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="w-6 h-6" />
                  Social Media Integration
                </CardTitle>
                <CardDescription>Connect your social media accounts</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Twitter className="w-5 h-5" />
                      <Label htmlFor="twitter-integration">Twitter Integration</Label>
                    </div>
                    <Switch
                      id="twitter-integration"
                      checked={twitterEnabled}
                      onCheckedChange={setTwitterEnabled}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Linkedin className="w-5 h-5" />
                      <Label htmlFor="linkedin-integration">LinkedIn Integration</Label>
                    </div>
                    <Switch
                      id="linkedin-integration"
                      checked={linkedinEnabled}
                      onCheckedChange={setLinkedinEnabled}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="flex justify-end"
          >
            <Button onClick={handleSaveSettings}>Save Settings</Button>
          </motion.div>
        </motion.div>
      </main>
      <Footer />
    </div>
  )
}

