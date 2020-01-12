const { h, Component, render } = window.preact

const GYM_ORDER = ['Kluuvi', 'Porthania', 'Kumpula', 'Meilahti', 'Otaniemi', 'Töölö', 'Viikki']

let showAllEvents = false
let allEvents = []
let filteredEvents = []

async function run() {
  const resp = await fetch('events.json')
  // const time = resp.headers.get('modified')
  const result = await resp.json()
  const time = result.currentTimeStamp
  const events = result.items
  allEvents = events.sort((a, b) => a.venue.localeCompare(b.venue))
  console.log(allEvents[0])
  console.log(allEvents[4])
  console.log(allEvents[12])
  renderApp(allEvents)
  if (time && time.length > 0) {
    renderLastModified(formatTimestamp(new Date(time)))
  }
}
function renderApp(events) {
  const app = h(
    'ul',
    { class: 'events-list' },
    events.map(event =>
      h('li',
        { class: `event ${getHidableClass(event)}` },
        [
          h('div', { class: 'event-header' }, [
            h('h3', null, event.venue),
            h('p', null, event.name),
            event.rooms.map(room => h('p', null, room))
          ]),
          h('div', { class: 'event-other' }, [
            event.onlyPrivateRegistrations && h('p', { class: 'private-event' }, 'Yksityinen'),
            h('p', null, 'Varauksia: ',
              h('span', { class: `reservations ${getColorForReservations(event)}` }, event.reservations)),
            h('p', null, `Maksimi: ${event.maxReservations}`),
            event.instructors.map(i => h('p', null, `${i.firstName} ${i.lastName}`))
          ]),
          h('div', { class: 'event-schedule' }, [
            h('p', null, 'Alkaa:'),
            h('time', null, formatTimestamp(new Date(event.startTime))),
            h('p', null, 'Loppuu:'),
            h('time', null, formatTimestamp(new Date(event.endTime))),
          ]),
          h('div', { class: 'event-reservation-schedule' }, [
            h('p', null, 'Alkaa:'),
            h('time', null, formatTimestamp(new Date(event.reservationPeriod.start))),
            h('p', null, 'Loppuu:'),
            h('time', null, formatTimestamp(new Date(event.reservationPeriod.end))),
          ]),
        ],
      )
    )
  )
  render(app, document.getElementById('events'))
}
function renderLastModified(lastModified) {
  const el = h(
    'b',
    null,
    lastModified
  )
  render(el, document.getElementById('timestamp'))
}
function getHidableClass(event) {
  console.log(event)
  console.log(event.onlyPrivateRegistrations)
  console.log(event.activity)
  if (event.onlyPrivateRegistrations || event.activity === 'Kuntosali') {
    return 'hidable hidden'
  }
  return ''
}
function getColorForReservations(event) {
  const difference = event.maxReservations - event.reservations
  if (event.maxReservations === 0) return ''
  else if (difference === 0) return 'red'
  else if (difference < 4) return 'orange'
  else if (difference < 10) return 'yellow'
  else return 'green'
}
function formatTimestamp(date) {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hours = date.getHours()
  const min = date.getMinutes()
  return `${hours > 9 ? hours : '0' + hours}:${min > 9 ? min : '0' + min} ${day}.${month}.${year}`
}
function filterGymAndPrivateEvents(events) {
  return events.filter(e => e.activity !== 'Kuntosali' && !e.onlyPrivateRegistrations)
}
function handleShowEventsToggle() {
  if (showAllEvents) {
    // Rerender with filtered
    document.querySelectorAll('.hidable').forEach(el => {
      el.classList.add('hidden')
    })
    document.querySelector('.toggle-events-btn').innerText = 'Näytä'
  } else {
    // Rerender with all
    document.querySelectorAll('.hidable').forEach(el => {
      el.classList.remove('hidden')
    })
    document.querySelector('.toggle-events-btn').innerText = 'Piilota'
  }
  showAllEvents = !showAllEvents
}

run()