"use client"

import * as React from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import axios from "axios"
import { useNavigate } from "react-router-dom"

// ---- backend endpoint ----
const BACKEND_URL = "http://127.0.0.1:8000"
const ENDPOINT = `${BACKEND_URL}/api/scanner-form`

// --- schema ---
// industry required; region/country optional but validated if non-empty
const formSchema = z.object({
  industry: z.string().min(2, "Industry is required").max(50, "Too long"),
  region: z
    .union([z.string().min(1, "Region is required"), z.literal("")])
    .optional(),
  country: z
    .union([
      z.string().min(2, "Country too short").max(50, "Too long"),
      z.literal(""),
    ])
    .optional(),
})
type FormValues = z.infer<typeof formSchema>

// --- static options ---
const INDUSTRY_OPTIONS = [
  "Finance",
  "Healthcare",
  "Technology",
  "Energy",
  "Consumer Goods",
  "Real Estate",
  "Education",
  "Transportation",
]
const REGION_OPTIONS = ["Americas", "EMEA", "APAC", "Latin America", "Africa"]
const COUNTRY_OPTIONS = [
  "Singapore",
  "United States",
  "United Kingdom",
  "Germany",
  "India",
  "Australia",
  "Japan",
  "Canada",
]

// --- helpers (safe) ---
const filterOptions = (query: string | undefined, list: string[]) =>
  !query
    ? list
    : list.filter((item) =>
        item.toLowerCase().includes(query.trim().toLowerCase())
      )
const exactMatch = (query: string | undefined, list: string[]) =>
  !!query && list.some((item) => item.toLowerCase() === query.trim().toLowerCase())

export default function IndustryRegionCountryForm() {
  const navigate = useNavigate()

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      industry: "",
      region: "",
      country: "",
    },
  })

  // normalize watched values
  const industryValRaw = watch("industry")
  const industryVal = typeof industryValRaw === "string" ? industryValRaw : ""
  const regionValRaw = watch("region")
  const regionVal = typeof regionValRaw === "string" ? regionValRaw : ""
  const countryValRaw = watch("country")
  const countryVal = typeof countryValRaw === "string" ? countryValRaw : ""

  const [industryFocused, setIndustryFocused] = React.useState(false)
  const [countryFocused, setCountryFocused] = React.useState(false)
  const [status, setStatus] = React.useState<string | null>(null)

  const industryMatches = filterOptions(industryVal, INDUSTRY_OPTIONS)
  const countryMatches = filterOptions(countryVal, COUNTRY_OPTIONS)
  const isExactIndustry = exactMatch(industryVal, INDUSTRY_OPTIONS)
  const isExactCountry = exactMatch(countryVal, COUNTRY_OPTIONS)

  const onSubmit = async (values: FormValues) => {
    const payload: Record<string, string | null> = {
      industry: values.industry,
    }

    payload.region = values.region ?? null
    payload.country = values.country ?? null

    try {
      console.log(payload)
      setStatus("Submitting...")
      const resp = await axios.post(ENDPOINT, payload, {
        headers: { "Content-Type": "application/json" },
        timeout: 5000,
      })
      setStatus("Submitted successfully.")
      console.log("Backend response:", resp.data)
      // redirect to dashboard
      navigate("/dashboard")
    } catch (err: any) {
      let msg = "Failed to submit"
      if (err.response) {
        msg = `Server error ${err.response.status}: ${
          typeof err.response.data === "string"
            ? err.response.data
            : JSON.stringify(err.response.data)
        }`
      } else if (err.request) {
        msg = "No response from server"
      } else if (err.message) {
        msg = err.message
      }
      setStatus(`Error: ${msg}`)
      console.error("Submission error:", err)
    }
  }

  return (
    <div className="form-root">
      <div className="card">
        <div className="header">
          <h2>Industry / Region / Country</h2>
          <p>Narrow down your view with industry, region and country filters.</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="form" noValidate>
          {/* Industry */}
          <div className="field">
            <label className="label">Industry</label>
            <div className="input-wrapper">
              <div className="icon">
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <circle cx="11" cy="11" r="7" />
                  <line x1="16.65" y1="16.65" x2="21" y2="21" />
                </svg>
              </div>
              <input
                type="text"
                placeholder="Search industry..."
                aria-label="Industry search"
                {...register("industry")}
                value={industryVal}
                onChange={(e) => setValue("industry", e.target.value)}
                onFocus={() => setIndustryFocused(true)}
                onBlur={() => setTimeout(() => setIndustryFocused(false), 150)}
                className="search-input"
              />
              {(industryFocused || (industryVal && !isExactIndustry)) && (
                <div className="dropdown">
                  {industryMatches.length === 0 && (
                    <div className="dropdown-empty">No industry found.</div>
                  )}
                  {industryMatches.map((opt) => (
                    <div
                      key={opt}
                      className={
                        opt.toLowerCase() === industryVal.trim().toLowerCase()
                          ? "dropdown-item selected"
                          : "dropdown-item"
                      }
                      onMouseDown={(e) => {
                        e.preventDefault()
                        setValue("industry", opt)
                        setIndustryFocused(false)
                      }}
                    >
                      {opt}
                    </div>
                  ))}
                </div>
              )}
            </div>
            {errors.industry && (
              <div className="error">{errors.industry.message}</div>
            )}
          </div>

          {/* Region (optional) */}
          <div className="field">
            <label className="label">Region</label>
            <div className="select-wrapper">
              <select
                aria-label="Region select"
                {...register("region")}
                value={regionVal}
                onChange={(e) => setValue("region", e.target.value)}
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  borderRadius: 12,
                  border: "1px solid #d1d5db",
                  fontSize: 14,
                  background: "#f9f9fc",
                  appearance: "none",
                  color: regionVal ? "#1f2d3a" : "#9ca3af",
                  boxSizing: "border-box" as const,
                  cursor: "pointer",
                }}
              >
                <option value="">Select a region</option>
                {REGION_OPTIONS.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
              <div className="select-icon">
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 20 20"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <polyline points="6 8 10 12 14 8" />
                </svg>
              </div>
            </div>
            {errors.region && (
              <div className="error">{errors.region.message}</div>
            )}
          </div>

          {/* Country (optional) */}
          <div className="field">
            <label className="label">Country</label>
            <div className="input-wrapper">
              <div className="icon">
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <circle cx="11" cy="11" r="7" />
                  <line x1="16.65" y1="16.65" x2="21" y2="21" />
                </svg>
              </div>
              <input
                type="text"
                placeholder="Search country..."
                aria-label="Country search"
                {...register("country")}
                value={countryVal}
                onChange={(e) => setValue("country", e.target.value)}
                onFocus={() => setCountryFocused(true)}
                onBlur={() => setTimeout(() => setCountryFocused(false), 150)}
                className="search-input"
              />
              {(countryFocused || (countryVal && !isExactCountry)) && (
                <div className="dropdown">
                  {countryMatches.length === 0 && (
                    <div className="dropdown-empty">No country found.</div>
                  )}
                  {countryMatches.map((opt) => (
                    <div
                      key={opt}
                      className={
                        opt.toLowerCase() === countryVal.trim().toLowerCase()
                          ? "dropdown-item selected"
                          : "dropdown-item"
                      }
                      onMouseDown={(e) => {
                        e.preventDefault()
                        setValue("country", opt)
                        setCountryFocused(false)
                      }}
                    >
                      {opt}
                    </div>
                  ))}
                </div>
              )}
            </div>
            {errors.country && (
              <div className="error">{errors.country.message}</div>
            )}
          </div>

          {status && (
            <div
              style={{
                fontSize: 12,
                marginBottom: 4,
                color: status.startsWith("Error") ? "#c92c2c" : "#1f6400",
              }}
            >
              {status}
            </div>
          )}

          <div className="submit-wrapper">
            <button
              type="submit"
              className="submit-btn"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Submitting..." : "Submit"}
            </button>
          </div>
        </form>
      </div>

      <style>{`
        .form-root {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 0 16px;
          background: #f2f4f9;
          font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .card {
          max-width: 500px;
          width: 100%;
          background: #ffffff;
          border-radius: 16px;
          padding: 32px;
          box-shadow: 0 25px 60px -10px rgba(100, 88, 255, 0.15);
        }
        .header h2 {
          font-size: 24px;
          font-weight: 600;
          margin: 0;
          color: #1f2d3a;
          text-align: left;
        }
        .header p {
          font-size: 12px;
          margin: 4px 0 24px;
          color: #4f5568;
          text-align: left;
        }
        .form {
          display: flex;
          flex-direction: column;
          gap: 24px;
        }
        .field {
          position: relative;
        }
        .label {
          display: block;
          margin-bottom: 6px;
          font-size: 12px;
          font-weight: 500;
          color: #4f5568;
          text-align: left;
        }
        .input-wrapper {
          position: relative;
        }
        .search-input {
          width: 100%;
          padding: 10px 12px 10px 40px;
          border-radius: 12px;
          border: 1px solid #d1d3db;
          font-size: 14px;
          outline: none;
          background: #f9f9fc;
          color: #1f2d3a;
          box-sizing: border-box;
        }
        .search-input::placeholder {
          color: #9ca3af;
        }
        .icon {
          position: absolute;
          left: 12px;
          top: 50%;
          transform: translateY(-50%);
          pointer-events: none;
          display: flex;
          align-items: center;
          color: #9ca3af;
        }
        .dropdown {
          position: absolute;
          top: 100%;
          left: 0;
          right: 0;
          margin-top: 4px;
          background: #fff;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          max-height: 220px;
          overflow-y: auto;
          z-index: 100;
          box-shadow: 0 10px 40px -10px rgba(100, 88, 255, 0.15);
        }
        .dropdown-item {
          padding: 10px 14px;
          cursor: pointer;
          font-size: 14px;
          color: #1f2d3a;
        }
        .dropdown-item.selected {
          background: #f0f0ff;
        }
        .dropdown-empty {
          padding: 10px 14px;
          color: #6b7280;
          font-size: 14px;
        }
        .select-wrapper {
          position: relative;
        }
        .select-icon {
          position: absolute;
          right: 12px;
          top: 50%;
          transform: translateY(-50%);
          pointer-events: none;
          display: flex;
          align-items: center;
          color: #374151;
        }
        .error {
          margin-top: 4px;
          font-size: 12px;
          color: #c92c2c;
        }
        .submit-wrapper {
          margin-top: 4px;
        }
        .submit-btn {
          width: 100%;
          padding: 14px 0;
          border-radius: 12px;
          background: linear-gradient(90deg, #6e5cff, #4f3acc);
          color: white;
          font-weight: 600;
          border: none;
          cursor: pointer;
          font-size: 16px;
        }
        .submit-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  )
}
