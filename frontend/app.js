const { h, Component, render } = window.preact

const GYM_ORDER = ['Kluuvi', 'Porthania', 'Kumpula', 'Meilahti', 'Otaniemi', 'Töölö', 'Viikki']

async function run() {
  const resp = await fetch('unisport.json')
  const gyms = await resp.json()
  renderApp(gyms.sort((a, b) => GYM_ORDER.indexOf(a.name) - GYM_ORDER.indexOf(b.name)))
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

run()