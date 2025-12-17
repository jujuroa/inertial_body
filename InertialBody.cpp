/*
 * InertialBody.cpp
 *
 *  Created on: Dec 16, 2025
 *      Author: youngh
 */

#include "InertialBody.h"

#include <cmath>

namespace easing {

InertialBody::InertialBody(double _elasticity, double _friction, double _mass,
                           double _distanceExponent)
    : elasticity(_elasticity),
      friction(_friction),
      mass(_mass),
      distanceExponent(_distanceExponent) {}

InertialBody::~InertialBody() {}

const InertialBody::InertialState& InertialBody::getCurrentStatus() const {
  return currentStatus;
}

void InertialBody::resetMovement() {
  this->currentStatus.reset();
}

InertialBody::InertialState InertialBody::step() {
  auto d = this->currentStatus.getDistance();
  auto spring = this->elasticity *
                std::copysign(std::pow(std::abs(d), this->distanceExponent), d);
  auto damping = this->friction * this->currentStatus.velocity;

  this->currentStatus.step((spring + damping) / this->mass);
  return this->currentStatus;
}

double InertialBody::getDistanceExponent() const {
  return distanceExponent;
}

void InertialBody::setDistanceExponent(double distanceExponent) {
  this->distanceExponent = distanceExponent;
}

double InertialBody::getElasticity() const {
  return elasticity;
}

void InertialBody::setElasticity(double elasticity) {
  this->elasticity = elasticity;
}

double InertialBody::getFriction() const {
  return friction;
}

void InertialBody::setFriction(double friction) {
  this->friction = friction;
}

double InertialBody::getMass() const {
  return mass;
}

void InertialBody::setMass(double mass) {
  this->mass = mass;
}

} /* namespace easing */
