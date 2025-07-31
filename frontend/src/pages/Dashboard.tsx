import { BellIcon } from "@heroicons/react/24/solid";

const alerts = [
  {
    id: 1,
    title: "New Lead: Acme Corp Expansion",
    description:
      "Acme Corp has posted new job listings in Singapore, signaling an upcoming office expansion.",
    avatar: "https://i.pravatar.cc/40?img=1",
  },
  {
    id: 2,
    title: "Industry Trend: Data Centers",
    description:
      "Surge in data center investments in the West region this quarter.",
    avatar: "https://i.pravatar.cc/40?img=2",
  },
  {
    id: 3,
    title: "Regulatory Filing: Beta Logistics",
    description:
      "Beta Logistics submitted a warehouse acquisition proposal in Johor.",
    avatar: "https://i.pravatar.cc/40?img=3",
  },
];

export default function DashboardPage() {
  return (
    <div className="bg-gray-50 py-16 sm:py-24">
      <div className="mx-auto max-w-2xl px-6 lg:max-w-7xl lg:px-8">
        <h2 className="text-center text-base/7 font-semibold text-indigo-600">
          Spot High-Growth Opportunities
        </h2>
        <p className="mx-auto mt-2 max-w-4xl text-center text-4xl font-semibold tracking-tight text-balance text-gray-950 sm:text-5xl">
          AI-Driven Market Intelligence for Real-Estate Deals
        </p>
        <div className="mt-10 grid gap-4 sm:mt-16 lg:grid-cols-3 lg:grid-rows-2">
          <div className="relative lg:row-span-2">
            <div className="absolute inset-px rounded-lg bg-white lg:rounded-l-4xl" />
            <div className="relative flex h-full flex-col overflow-hidden rounded-[calc(var(--radius-lg)+1px)] lg:rounded-l-[calc(2rem+1px)]">
              <div className="px-8 pt-8 pb-3 sm:px-10 sm:pt-10 sm:pb-0">
                <p className="mt-2 text-lg font-medium tracking-tight text-gray-950 max-lg:text-center">
                  Data Ingestion
                </p>
                <p className="mt-2 max-w-lg text-sm/6 text-gray-600 max-lg:text-center">
                  Continuously pull and normalize data from reliable CapitaLand
                  data sources, news outlets, and regulatory filings.
                </p>
              </div>
              <div className="@container relative min-h-120 w-full grow max-lg:mx-auto max-lg:max-w-sm">
                <div className="absolute inset-x-10 top-10 bottom-0 overflow-hidden rounded-t-[12cqw] border-x-[3cqw] border-t-[3cqw] border-gray-700 bg-gray-900 shadow-2xl">
                  <img
                    alt=""
                    src="https://tailwindcss.com/plus-assets/img/component-images/bento-03-mobile-friendly.png"
                    className="size-full object-cover object-top"
                  />
                </div>
              </div>
            </div>
            <div className="pointer-events-none absolute inset-px rounded-lg shadow-sm outline outline-black/5 lg:rounded-l-4xl" />
          </div>
          <div className="relative max-lg:row-start-1">
            <div className="absolute inset-px rounded-lg bg-white max-lg:rounded-t-4xl" />
            <div className="relative flex h-full flex-col overflow-hidden rounded-[calc(var(--radius-lg)+1px)] max-lg:rounded-t-[calc(2rem+1px)]">
              <div className="px-8 pt-8 sm:px-10 sm:pt-10">
                <p className="mt-2 text-lg font-medium tracking-tight text-gray-950 max-lg:text-center">
                  Real-time Signal Detection
                </p>
                <p className="mt-2 max-w-lg text-sm/6 text-gray-600 max-lg:text-center">
                  Classify industries with AI and flag company expansions or
                  relocations within minutes.
                </p>
              </div>
              <div className="flex flex-1 items-center justify-center px-8 max-lg:pt-10 max-lg:pb-12 sm:px-10 lg:pb-2">
                <img
                  alt=""
                  src="https://tailwindcss.com/plus-assets/img/component-images/bento-03-performance.png"
                  className="w-full max-lg:max-w-xs"
                />
              </div>
            </div>
            <div className="pointer-events-none absolute inset-px rounded-lg shadow-sm outline outline-black/5 max-lg:rounded-t-4xl" />
          </div>
          <div className="relative max-lg:row-start-3 lg:col-start-2 lg:row-start-2">
            <div className="absolute inset-px rounded-lg bg-white" />
            <div className="relative flex h-full flex-col overflow-hidden rounded-[calc(var(--radius-lg)+1px)]">
              <div className="px-8 pt-8 sm:px-10 sm:pt-10">
                <p className="mt-2 text-lg font-medium tracking-tight text-gray-950 max-lg:text-center">
                  Asset Mapping
                </p>
                <p className="mt-2 max-w-lg text-sm/6 text-gray-600 max-lg:text-center">
                  Translate corporate moves into the right real-estate asset
                  classes (office, logistics, retail, data center).
                </p>
              </div>
              <div className="@container flex flex-1 items-center max-lg:py-6 lg:pb-2">
                <img
                  alt=""
                  src="https://tailwindcss.com/plus-assets/img/component-images/bento-03-security.png"
                  className="h-[min(152px,40cqw)] object-cover"
                />
              </div>
            </div>
            <div className="pointer-events-none absolute inset-px rounded-lg shadow-sm outline outline-black/5" />
          </div>
          <div className="relative lg:row-span-2">
            <div className="absolute inset-px rounded-lg bg-white max-lg:rounded-b-4xl lg:rounded-r-4xl" />
            <div className="relative flex h-full flex-col overflow-hidden rounded-[calc(var(--radius-lg)+1px)] max-lg:rounded-b-[calc(2rem+1px)] lg:rounded-r-[calc(2rem+1px)]">
              <div className="px-8 pt-8 pb-3 sm:px-10 sm:pt-10 sm:pb-0">
                <p className="mt-2 text-lg font-medium tracking-tight text-gray-950 max-lg:text-center">
                  Actionable Alerts
                </p>
                <p className="mt-2 max-w-lg text-sm/6 text-gray-600 max-lg:text-center">
                  Notify your team via email or Slack with top-scoring leads,
                  contact info, and source citations.
                </p>
                <p className="mt-2 max-w-lg text-sm/6 text-gray-600 max-lg:text-center">
                  Each alert will include a direct link to the original source,
                  a confidence score indicating growth momentum, and a clear
                  recommended next step (e.g., “Schedule site visit”).
                </p>
              </div>
              <div className="grid grid-cols-1 gap-4 p-6">
                {alerts.map((alert) => (
                  <div
                    key={alert.id}
                    className="flex items-start space-x-3 bg-white p-4 rounded-lg shadow"
                  >
                    <img
                      src={alert.avatar}
                      alt="Profile"
                      className="h-10 w-10 rounded-full"
                    />
                    <div className="flex-1">
                      <h4 className="text-sm font-semibold text-gray-900">
                        {alert.title}
                      </h4>
                      <p className="mt-1 text-sm text-gray-600">
                        {alert.description}
                      </p>
                    </div>
                    <BellIcon className="h-6 w-6 text-indigo-500" />
                  </div>
                ))}
              </div>
            </div>
            <div className="pointer-events-none absolute inset-px rounded-lg shadow-sm outline outline-black/5 max-lg:rounded-b-4xl lg:rounded-r-4xl" />
          </div>
        </div>
        {/* TODO: Add in code to display data tables below */}
      </div>
    </div>
  );
}
