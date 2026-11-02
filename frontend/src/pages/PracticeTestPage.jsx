import { useParams, Link, useNavigate } from 'react-router-dom'
import { ArrowLeft, PlayCircle, Clock, ChevronRight, Book} from 'lucide-react'
import { useState, useEffect } from 'react'
import { sessionsApi, testsApi } from '../utils/api'
import toast from 'react-hot-toast'
import { ReadingIcon, ListeningIcon, WritingIcon, SpeakingIcon } from '../components/ExamIcons'
import { LoadingScreen } from '../components/ui'

const MODULES = [
  { type: 'reading',   icon: ReadingIcon,   label: 'Reading',   time: '60 min', desc: '3 passages · 40 questions',  accent: '#1d4ed8', bg: '#eff6ff' },
  { type: 'listening', icon: ListeningIcon, label: 'Listening', time: '30 min', desc: '4 sections · 40 questions',  accent: '#0369a1', bg: '#f0f9ff' },
  { type: 'writing',   icon: WritingIcon,   label: 'Writing',   time: '60 min', desc: '2 tasks · 150 & 250 words',  accent: '#7c3aed', bg: '#f5f3ff' },
  { type: 'speaking',  icon: SpeakingIcon,  label: 'Speaking',  time: '15 min', desc: '3 parts · face-to-face',    accent: '#b45309', bg: '#fffbeb' },
]

export default function PracticeTestPage() {
  const { bookId } = useParams()
  const navigate = useNavigate()
  const [starting, setStarting] = useState(null)
  const [tests, setTests] = useState([])
  const [loading, setLoading] = useState(true)

  const bookNum = parseInt(bookId, 10) || 1

  useEffect(() => {
    const fetchTests = async () => {
      try {
        const response = await testsApi.listTests(bookId)
        setTests(response.data)
      } catch (error) {
        toast.error('Failed to load tests')
      } finally {
        setLoading(false)
      }
    }
    fetchTests()
  }, [bookId])

  const startModule = async (testId, moduleType) => {
    const key = `${testId}-${moduleType}`
    if (starting) return
    setStarting(key)
    try {
      await sessionsApi.start({ test_id: testId, section_type: moduleType })
      navigate(`/test/${testId}/${moduleType}`)
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to start'
      if (msg.toLowerCase().includes('premium')) {
        toast.error('This test requires a Premium subscription')
        navigate('/pricing')
      } else {
        toast.error(msg)
      }
    } finally {
      setStarting(null)
    }
  }

  const moduleCounts = MODULES.length
  const totalModules = tests.length * moduleCounts

  if (loading) {
    return <LoadingScreen message="Loading practice tests..." />
  }

  return (
    <div
      className="min-h-screen"
      
    >
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');

      `}</style>

      <div className="space-y-6 sm:space-y-8 page-fade">

        {/* ── Hero header ── */}
        <div className="relative  overflow-hidden" style={{ background: '#ffffff' }}>
          
          <div className="relative px-5 sm:px-7 py-5 sm:py-7 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 sm:gap-5">
            <div className="flex items-center gap-4">
              <Link
                to="/book"
                className="p-2  text-gray-400 hover:text-red-700 hover:bg-red-50 transition-colors shrink-0"
              >
                <ArrowLeft size={18} />
              </Link>
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-semibold text-red-400 uppercase tracking-widest">
                    Book {bookNum}
                  </span>
                  <span className="text-gray-200">/</span>
                  <span className="text-xs font-semibold text-red-400 uppercase tracking-widest">
                    {totalModules} Modules
                  </span>
                </div>
                <h1
                  className="text-2xl sm:text-3xl font-bold text-gray-900 leading-tight"
                  
                >
                  Practice Tests
                </h1>
                <p className="text-sm text-gray-400 mt-1.5 leading-relaxed">
                  {tests.length} full tests · {MODULES.map(m => m.label).join(', ')} — all at your pace.
                </p>
              </div>
            </div>
            <Link
              to="/book"
              className="shrink-0 inline-flex items-center gap-1.5 text-xs font-semibold text-red-700 hover:text-red-800 transition-colors"
            >
              <Book size={14} /> All Books <ChevronRight size={13} />
            </Link>
          </div>
        </div>


        {/* ── Module legend ── */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {MODULES.map(({ icon: Icon, label, time, accent, bg }) => (
            <div key={label} className="bg-white  border border-gray-100 p-4 flex items-center gap-3 hover:shadow-sm transition-shadow">
              <Icon size={15} color={accent} />
              <div className="min-w-0">
                <p className="text-sm font-bold text-gray-900 leading-tight" >
                  {label}
                </p>
                <p className="text-xs text-gray-400 mt-0.5">{time}</p>
              </div>
            </div>
          ))}
        </div>

        {/* ── Tests ── */}
        <div className="space-y-4 sm:space-y-5">
          {tests.map((test) => (
            <div
              key={test.id}
              className="bg-white  border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
            >
              {/* Test header */}
              <div className="flex items-center justify-between px-5 sm:px-6 py-4 border-b border-gray-50">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8  flex items-center justify-center text-sm font-bold" style={{ background: '#fff1f1', color: '#CC0000'}}>
                    {test.test_number}
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-gray-900" >
                      {test.title}
                    </h3>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {moduleCounts} modules · {
                        MODULES.reduce((acc, m) => {
                          const mins = parseInt(m.time)
                          return acc + (isNaN(mins) ? 0 : mins)
                        }, 0)
                      } min total
                    </p>
                  </div>
                </div>
                <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2.5 py-1  bg-green-50 text-green-700 border border-green-200">
                  <PlayCircle size={10} /> start test
                </span>
              </div>

              {/* Module buttons */}
              <div className="grid grid-cols-2 lg:grid-cols-4 divide-x divide-y lg:divide-y-0 divide-gray-50">
                {MODULES.map(({ type, icon: Icon, label, time, desc, accent, bg }) => {
                  const key = `${test.id}-${type}`
                  const busy = starting === key

                  return (
                    <button
                      key={type}
                      onClick={() => startModule(test.id, type)}
                      disabled={busy}
                      className={`relative flex flex-col p-5 text-left transition-all duration-150 ${
                        busy ? 'cursor-wait' : 'cursor-pointer hover:bg-gray-50 active:scale-[0.98]'
                      }`}
                    >
                      <div className="flex items-center gap-3 mb-3">
                        {busy ? (
                          <div className="w-4 h-4 border-2 animate-spin shrink-0" style={{ borderColor: `${accent}40`, borderTopColor: accent }} />
                        ) : (
                          <Icon size={17} color={accent} />
                        )}
                      </div>
                      <div className="min-w-0">
                        <p className="text-sm font-bold text-gray-900 leading-tight" >
                          {label}
                        </p>
                          <div className="flex items-center gap-1 mt-0.5">
                            <Clock size={10} className="text-gray-300" />
                            <span className="text-[10px] text-gray-400">{time}</span>
                        </div>
                      </div>

                      <p className="text-xs text-gray-400 leading-relaxed mb-3 line-clamp-2">{desc}</p>

                      <div className="mt-auto flex items-center gap-1.5 text-xs font-semibold" style={{ color: accent }}>
                        {busy ? 'Starting…' : 'Start Practice'}
                        {!busy && <ChevronRight size={12} />}
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          ))}
        </div>

        {/* ── Bottom CTA ── */}
        <div
          className="relative  overflow-hidden px-5 sm:px-7 py-5 sm:py-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
          style={{ background: '#ffffff', border: '1px solid #ffffff' }}
        >
          
          <div>
            <div className="flex items-center gap-2 mb-1">
              <ReadingIcon size={14} color="#CC0000" />
              <span className="text-xs font-bold text-red-700 uppercase tracking-widest">Book {bookNum}</span>
            </div>
            <h3 className="text-base font-bold text-gray-900" >
              Master all {totalModules} modules
            </h3>
            <p className="text-xs text-gray-500 mt-0.5">
              Consistent practice with timed tests boosts your band score by <strong className="text-gray-700">0.5–1.5 bands</strong>.
            </p>
          </div>
          <Link
            to="/tests"
            className="shrink-0 inline-flex items-center gap-2 px-5 py-2.5  text-sm font-bold transition-all hover:-translate-y-0.5"
            style={{ background: '#CC0000', color: '#fff' }}
          >
            Browse All Tests <ChevronRight size={15} />
          </Link>
        </div>

      </div>
    </div>
  )
}
