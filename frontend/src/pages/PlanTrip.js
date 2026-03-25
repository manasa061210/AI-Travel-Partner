import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { aiApi, userApi } from '../services/api';
import './PlanTrip.css';

const INTERESTS_LIST = ['Adventure', 'Relaxation', 'Cultural', 'Beach', 'Mountain', 'City', 'Food', 'Shopping', 'Wildlife', 'Spiritual'];
const STEPS = ['Destination & Basics', 'Preferences', 'Generating Plan'];

function PlanTrip() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [loadingMsg, setLoadingMsg] = useState('');
  const [error, setError] = useState('');
  const [budgetEst, setBudgetEst] = useState(null);

  const [form, setForm] = useState({
    destination: searchParams.get('destination') || '',
    days: 3,
    travelers: 1,
    start_date: '',
    budget: 15000,
    interests: [],
    hotel_category: 'standard',
    transport_type: 'flight',
    season: 'normal',
  });

  const update = (field, value) => setForm(prev => ({ ...prev, [field]: value }));

  const toggleInterest = (i) => {
    const lower = i.toLowerCase();
    setForm(prev => ({
      ...prev,
      interests: prev.interests.includes(lower)
        ? prev.interests.filter(x => x !== lower)
        : [...prev.interests, lower],
    }));
  };

  // Live budget estimate on step 1
  useEffect(() => {
    if (step === 1 && form.destination) {
      aiApi.estimateBudget({
        days: form.days,
        destination: form.destination,
        hotel_category: form.hotel_category,
        transport_type: form.transport_type,
        season: form.season,
        travelers: form.travelers,
      }).then(res => setBudgetEst(res.data.data)).catch(() => {});
    }
  }, [step, form.days, form.hotel_category, form.transport_type, form.season, form.travelers, form.destination]);

  const loadingMessages = [
    '🔍 Analyzing your preferences...',
    '🗺️ Finding best attractions...',
    '📍 Optimizing routes with Dijkstra\'s algorithm...',
    '💰 Calculating budget breakdown...',
    '📅 Scheduling day-by-day activities...',
    '✨ Finalizing your personalized itinerary...',
  ];

  const generatePlan = async () => {
    setStep(2);
    setLoading(true);
    setError('');

    // Cycle loading messages
    let msgIdx = 0;
    setLoadingMsg(loadingMessages[0]);
    const interval = setInterval(() => {
      msgIdx = (msgIdx + 1) % loadingMessages.length;
      setLoadingMsg(loadingMessages[msgIdx]);
    }, 1200);

    try {
      const res = await aiApi.generateItinerary(form);
      clearInterval(interval);
      const itinerary = res.data.data;

      // Save trip
      const saveRes = await userApi.saveTrip({
        destination: form.destination,
        days: form.days,
        travelers: form.travelers,
        start_date: form.start_date,
        budget: form.budget,
        interests: form.interests,
        hotel_category: form.hotel_category,
        transport_type: form.transport_type,
        plan: itinerary,
        total_cost: itinerary.budget_estimate?.total || itinerary.total_cost || form.budget,
        title: `${form.days}-Day Trip to ${form.destination}`,
      });

      navigate(`/itinerary/${saveRes.data.data.id}`, { state: { itinerary } });
    } catch (err) {
      clearInterval(interval);
      setError(err.response?.data?.message || 'Failed to generate itinerary. Please try again.');
      setStep(1);
      setLoading(false);
    }
  };

  return (
    <div className="plan-trip">
      {/* Step Indicator */}
      <div className="plan-hero">
        <div className="container">
          <h1>Plan Your Trip ✈️</h1>
          <p>Let AI craft a personalized itinerary just for you</p>
          <div className="step-indicator">
            {STEPS.map((s, i) => (
              <div key={i} className={`step-item ${i === step ? 'active' : i < step ? 'done' : ''}`}>
                <div className="step-circle">{i < step ? '✓' : i + 1}</div>
                <span>{s}</span>
                {i < STEPS.length - 1 && <div className="step-line" />}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="container plan-body">
        {/* Step 0: Destination & Basics */}
        {step === 0 && (
          <div className="plan-card">
            <h2>Where are you going? 🌍</h2>
            <p className="card-subtitle">Enter your destination and trip basics</p>

            <div className="plan-form">
              <div className="form-group full">
                <label>Destination *</label>
                <input type="text" placeholder="e.g. Goa, Manali, Jaipur, Kerala..."
                  value={form.destination} onChange={e => update('destination', e.target.value)} required />
              </div>

              <div className="form-group">
                <label>Number of Days: <strong>{form.days}</strong></label>
                <input type="range" min="1" max="14" value={form.days}
                  onChange={e => update('days', parseInt(e.target.value))} className="slider" />
                <div className="slider-labels"><span>1 day</span><span>14 days</span></div>
              </div>

              <div className="form-group">
                <label>Travelers: <strong>{form.travelers}</strong></label>
                <input type="range" min="1" max="10" value={form.travelers}
                  onChange={e => update('travelers', parseInt(e.target.value))} className="slider" />
                <div className="slider-labels"><span>1</span><span>10</span></div>
              </div>

              <div className="form-group">
                <label>Start Date</label>
                <input type="date" value={form.start_date}
                  min={new Date().toISOString().split('T')[0]}
                  onChange={e => update('start_date', e.target.value)} />
              </div>

              <div className="form-group">
                <label>Total Budget (₹)</label>
                <input type="number" value={form.budget}
                  onChange={e => update('budget', parseInt(e.target.value))}
                  min="1000" step="500" placeholder="15000" />
              </div>
            </div>

            <div className="plan-actions">
              <button className="btn-next" onClick={() => {
                if (!form.destination.trim()) return alert('Please enter a destination');
                setStep(1);
              }}>Next: Preferences →</button>
            </div>
          </div>
        )}

        {/* Step 1: Preferences */}
        {step === 1 && (
          <div className="plan-step1-layout">
            <div className="plan-card">
              <h2>Customize Your Experience 🎯</h2>
              <p className="card-subtitle">Tell us what you enjoy</p>

              <div className="plan-form">
                <div className="form-group full">
                  <label>Interests</label>
                  <div className="interests-grid">
                    {INTERESTS_LIST.map(i => (
                      <button type="button" key={i}
                        className={`interest-tag ${form.interests.includes(i.toLowerCase()) ? 'selected' : ''}`}
                        onClick={() => toggleInterest(i)}>{i}</button>
                    ))}
                  </div>
                </div>

                <div className="form-group">
                  <label>Hotel Category</label>
                  <div className="option-group">
                    {['budget', 'standard', 'luxury'].map(h => (
                      <button key={h} type="button"
                        className={`option-btn ${form.hotel_category === h ? 'selected' : ''}`}
                        onClick={() => update('hotel_category', h)}>
                        {h === 'budget' ? '💸 Budget' : h === 'standard' ? '🏨 Standard' : '👑 Luxury'}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="form-group">
                  <label>Transport Type</label>
                  <div className="option-group">
                    {[['flight','✈️ Flight'],['train','🚂 Train'],['bus','🚌 Bus'],['car','🚗 Car']].map(([v, l]) => (
                      <button key={v} type="button"
                        className={`option-btn ${form.transport_type === v ? 'selected' : ''}`}
                        onClick={() => update('transport_type', v)}>{l}</button>
                    ))}
                  </div>
                </div>

                <div className="form-group">
                  <label>Season</label>
                  <div className="option-group">
                    {[['normal','🌤 Normal'],['peak','📈 Peak'],['off-peak','📉 Off-Peak']].map(([v, l]) => (
                      <button key={v} type="button"
                        className={`option-btn ${form.season === v ? 'selected' : ''}`}
                        onClick={() => update('season', v)}>{l}</button>
                    ))}
                  </div>
                </div>
              </div>

              <div className="plan-actions">
                <button className="btn-back" onClick={() => setStep(0)}>← Back</button>
                <button className="btn-generate" onClick={generatePlan}>
                  🤖 Generate AI Itinerary
                </button>
              </div>
            </div>

            {/* Budget Estimator */}
            {budgetEst && (
              <div className="budget-sidebar">
                <h3>💰 Budget Estimate</h3>
                <p className="dest-label">{form.destination} · {form.days} days · {form.travelers} traveller{form.travelers > 1 ? 's' : ''}</p>

                <div className="budget-total">
                  ₹{budgetEst.total?.toLocaleString()}
                  <span>₹{budgetEst.per_person?.toLocaleString()}/person</span>
                </div>

                <div className="budget-bars">
                  {Object.entries(budgetEst.breakdown || {}).map(([key, val]) => {
                    const pct = Math.round((val / budgetEst.total) * 100);
                    const colors = { accommodation: '#3949ab', transport: '#00acc1', food: '#43a047', activities: '#ff6f00', misc: '#9e9e9e' };
                    return (
                      <div key={key} className="budget-bar-row">
                        <div className="bar-label">
                          <span style={{ textTransform: 'capitalize' }}>{key}</span>
                          <span>₹{val?.toLocaleString()} ({pct}%)</span>
                        </div>
                        <div className="bar-track">
                          <div className="bar-fill" style={{ width: `${pct}%`, background: colors[key] || '#ccc' }} />
                        </div>
                      </div>
                    );
                  })}
                </div>

                <div className="budget-note">
                  {budgetEst.notes?.season_adjustment !== '0%' && (
                    <p>📈 {budgetEst.notes?.season} season: {budgetEst.notes?.season_adjustment} adjustment</p>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Step 2: Loading */}
        {step === 2 && (
          <div className="plan-card generating-card">
            <div className="generating-animation">
              <div className="gen-spinner" />
            </div>
            <h2>Creating Your Personalized Itinerary</h2>
            <p className="gen-msg">{loadingMsg}</p>

            {error && (
              <div className="auth-error" style={{ maxWidth: 400, margin: '20px auto 0' }}>
                ⚠️ {error}
              </div>
            )}

            <div className="algo-steps">
              <div className="algo-step">🧠 NLP Preference Analysis</div>
              <div className="algo-step">🎯 Content-Based Filtering</div>
              <div className="algo-step">🗺️ Dijkstra Route Optimization</div>
              <div className="algo-step">📅 Greedy Activity Scheduling</div>
              <div className="algo-step">💰 Linear Regression Budget Model</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PlanTrip;
