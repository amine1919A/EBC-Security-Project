FROM sonarqube:community

ENV SONAR_CE_JAVAOPTS="-Xmx512m"
ENV SONAR_SEARCH_JAVAOPTS="-Xmx512m"
ENV SONAR_WEB_JAVAOPTS="-Xmx512m"

COPY rules/ /opt/sonarqube/extensions/rules/
