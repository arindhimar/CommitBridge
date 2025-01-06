import React, { createContext, useContext, useState } from 'react'
import { AlertCircle, CheckCircle, Info, X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const AlertContext = createContext(undefined)

export const useAlert = () => {
  const context = useContext(AlertContext)
  if (!context) {
    throw new Error('useAlert must be used within an AlertProvider')
  }
  return context
}

export const AlertProvider = ({ children }) => {
  const [alert, setAlert] = useState(null)

  const showAlert = (type, message) => {
    setAlert({ type, message })
  }

  const hideAlert = () => {
    setAlert(null)
  }

  return (
    <AlertContext.Provider value={{ showAlert, hideAlert }}>
      {children}
      <AnimatePresence>
        {alert && (
          <motion.div
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
            className="fixed top-4 right-4 z-50"
          >
            <div className={`p-4 rounded-md shadow-md flex items-center ${
              alert.type === 'success' ? 'bg-green-100 text-green-800' :
              alert.type === 'error' ? 'bg-red-100 text-red-800' :
              alert.type === 'warning' ? 'bg-yellow-100 text-yellow-800' :
              'bg-blue-100 text-blue-800'
            }`}>
              {alert.type === 'success' && <CheckCircle className="w-5 h-5 mr-2" />}
              {alert.type === 'error' && <AlertCircle className="w-5 h-5 mr-2" />}
              {alert.type === 'warning' && <AlertCircle className="w-5 h-5 mr-2" />}
              {alert.type === 'info' && <Info className="w-5 h-5 mr-2" />}
              <span>{alert.message}</span>
              <button onClick={hideAlert} className="ml-4">
                <X className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </AlertContext.Provider>
  )
}

