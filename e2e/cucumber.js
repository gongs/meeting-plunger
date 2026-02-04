export default {
  default: {
    require: ['steps/**/*.js', 'support/**/*.js'],
    requireModule: [],
    format: ['progress', 'html:reports/cucumber-report.html', 'json:reports/cucumber-report.json'],
    formatOptions: { snippetInterface: 'async-await' },
    publishQuiet: true,
  },
};
