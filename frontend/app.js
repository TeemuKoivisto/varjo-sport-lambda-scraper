const { h, Component, render } = window.preact

const GYM_ORDER = ['Kluuvi', 'Porthania', 'Kumpula', 'Meilahti', 'Otaniemi', 'Töölö', 'Viikki']

async function run() {
  const resp = await fetch('unisport.json')
  const lastModified = resp.headers.get('last-modified')
  const gyms = await resp.json()
  const sorted = gyms.sort((a, b) => GYM_ORDER.indexOf(a.name) - GYM_ORDER.indexOf(b.name))
  renderApp(sorted)
  if (lastModified && lastModified.length > 0) {
    renderLastModified(formatTimestamp(new Date(lastModified)))
  }
}
function renderApp(gyms) {
  const app = h(
    'div',
    { class: 'gyms-container' },
    gyms.map(gym =>
      h('div',
        { class: 'gym' },
        [
          h('a',
          { href: gym.orig_url, rel: "noopener", target:"_blank" },
            h('h2', { class: 'name-header', id: gym.name }, gym.name)
          ),
          h('p', { class: 'info-text' }, gym.info),
          h('h3', { class: 'normal-hours-header' }, gym.normal_hours_header),
          h('ul', { class: 'normal-hours' }, gym.normal_hours.map(hour => h('li', null, hour))),
          h('h3', { class: 'sauna-hours-header' }, 'Saunat'),
          h('ul', { class: 'sauna-hours' }, gym.sauna_hours.map(hour => h('li', null, hour))),
          h('h3', { class: 'exception-hours-header' }, 'Poikkeusaukioloajat'),
          h('ul', { class: 'exception-hours' }, gym.exception_hours.map(hour => h('li', null, hour))),
        ],
      )
    )
  )
  render(app, document.getElementById('gyms'))
}
function renderLastModified(lastModified) {
  const el = h(
    'b',
    null,
    lastModified
  )
  render(el, document.getElementById('timestamp'))
}
function formatTimestamp(date) {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hours = date.getHours()
  const min = date.getMinutes()
  return `${hours > 9 ? hours : '0' + hours}:${min > 9 ? min : '0' + min} ${day}.${month}.${year}`
}

run()